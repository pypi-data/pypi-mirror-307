/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable no-mixed-spaces-and-tabs */
import * as semver from 'semver';
import { v4 as uuidv4 } from 'uuid';
import getTheme from './theme';
import { CopilotCapabilities } from './CopilotCapabilitiesEnum';
import { showErorrView } from './errorView';
import PiecesOSUpdating from './PiecesOSUpdating';
import { NotificationParameters } from './types/NotificationParameters';
import { OSAppletEnum } from '@pieces.app/pieces-os-client';
import { launchRuntime } from '../../../actions/launch_runtime';
import ConnectorSingleton from '../../../connection/connector_singleton';
import { copilotParams, copilotState } from './params';
import PiecesCacheSingleton from '../../../cache/pieces_cache';
import showExportedSnippet from '../../snippetExportView';
import { defaultApp } from '../../..';

export default async function initCopilot() {
  connectionPoller();

  const iframe = document.createElement('iframe');

  iframe.id = 'pieces-copilot';
  iframe.name = 'pieces-copilot';
  iframe.setAttribute(
    'style',
    'width: 100%; height: 100%; margin: 0px; overflow: hidden; border: none;'
  );
  iframe.setAttribute('allow', 'clipboard-read; clipboard-write;');

  const url = await getCopilotUrl();
  iframe.src = url.href;

  document.getElementById('gpt-tab')?.appendChild(iframe);

  const observer = new MutationObserver(async () => {
    iframe.contentWindow?.postMessage(
      {
        type: 'setTheme',
        destination: 'webview',
        data: getTheme(),
      },
      '*'
    );
  });
  observer.observe(document.body, { attributes: true });
}
/*
  Entry point for the copilot webview
  - sets up async message post / rec so we can turn a req/res pair into a promise
*/
const messageMap = new Map<
  string,
  { resolve: (any: any) => any; reject: (any: any) => any }
>();
export const port = navigator.userAgent.toLowerCase().includes('linux')
  ? 5323
  : 1000;
// this lives here instead of version check so we don't need to do message passing.
export let migration: number;
export const schemaNumber = 0;
let resolveLoading: () => void;
export const loadingPromise: Promise<void> = new Promise(
  (resolve) => (resolveLoading = resolve)
);
const minimumVersion = '10.0.0';
const maximumVersion = '11.0.0';

export function launchPos() {
  launchRuntime();
}

export function getNextMessageId() {
  return uuidv4();
}

async function handleWebviewMessage(event: MessageEvent<any>) {
  if (event.data.type === 'displayNotification') {
    const params: NotificationParameters = {
      actions: event.data.data.actions,
      message: event.data.data.message,
      title: event.data.data.title,
      type:
        event.data.data.type === 'warning'
          ? 'warn'
          : event.data.data.type === 'success' ||
            event.data.data.type === 'information'
          ? 'info'
          : 'error',
    };
    copilotParams.sendNotification(params);
    return;
  }

  if (event.data.type === 'copyToClipboard') {
    window.navigator.clipboard.writeText(event.data.data);
    return;
  }

  let timeoutId: NodeJS.Timeout | undefined = undefined;
  if (event.data.type === 'persistState') {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      copilotParams.saveState(JSON.stringify(event.data.data));
    }, 200);
    return;
  }

  if (event.data.type === 'insertAtCursor') {
    if (typeof event.data.data !== 'string')
      throw new Error('invalid insert at cursor data');
    copilotParams.insertAtCursor(event.data.data);
  }

  if (event.data.type === 'previewAsset') {
    let snippetData =
      PiecesCacheSingleton.getInstance().mappedAssets[event.data.data];
    if (!snippetData) {
      setTimeout(() => {
        snippetData =
          PiecesCacheSingleton.getInstance().mappedAssets[event.data.data];
        showExportedSnippet({
          snippetData:
            PiecesCacheSingleton.getInstance().mappedAssets[event.data.data],
        });
      }, 300);
    } else
      showExportedSnippet({
        snippetData:
          PiecesCacheSingleton.getInstance().mappedAssets[event.data.data],
      });
    return;
  }
  if (event.data.type === 'openSettings') {
    defaultApp.commands.execute('settingeditor:open', { query: 'pieces' });
  }
  if (event.data.type === 'launchPos') {
    launchPos();
  }
}

export async function postToFrame(message: { [key: string]: any }) {
  const iframe = document.getElementById(
    'pieces-copilot'
  ) as HTMLIFrameElement | null;
  if (!iframe) throw new Error('pieces-copilot id is missing on the iframe');
  await loadingPromise;

  iframe.contentWindow?.postMessage(message, '*');
}

/**
 * Handles incoming message from the backend. Resolves/rejects promises based on the message id.
 * @param event - The message sent from the backend of type {@link CopilotMessageData}
 */
async function handleMessage(event: MessageEvent<any>) {
  if (event.data.type === 'loaded') {
    console.log('resolved loading');
    // setTimeout(resolveLoading, 400);
    resolveLoading();
  }
  if (event.data.destination === 'extension') handleWebviewMessage(event);

  // we are adding context to the current conversation
  if (event.data.action === 'addAnchorToContext') {
    return postToFrame({
      type: 'addToContext',
      data: event.data.directory
        ? {
            action: 'addAnchorsToContext',
            directories: [event.data.path],
            files: [],
          }
        : {
            action: 'addAnchorsToContext',
            files: [event.data.path],
            directories: [],
          },
      destination: 'webview',
    });
  }
  if (event.data.action === 'addSnippetToContext') {
    return postToFrame({
      type: 'addToContext',
      data: {
        action: 'addSnippetsToContext',
        assets: [event.data.asset],
      },
      destination: 'webview',
    });
  }
  const message = event.data;
  // this is the 'ask copilot about' flow
  if (message.type === 'performQuery') {
    postToFrame({
      type: 'askCopilot',
      data: message.data,
      destination: 'webview',
    });
    return;
  }

  const id = message.id;
  const handler = messageMap.get(id);
  if (message.error) {
    handler?.reject(message.error);
  } else {
    handler?.resolve(message.data);
  }
  messageMap.delete(id);
}

async function checkForConnection() {
  return ConnectorSingleton.getInstance()
    .wellKnownApi.getWellKnownHealth()
    .then(() => true)
    .catch(() => false);
}

async function setIframeUrl() {
  const iframe = document.getElementById(
    'pieces-copilot'
  ) as HTMLIFrameElement | null;

  if (!iframe) throw new Error('Iframe is not present');
  const url = await getCopilotUrl();
  iframe.src = url.href;
}

async function connectionPoller(): Promise<void> {
  const connected = await checkForConnection();

  let version = await ConnectorSingleton.getInstance()
    .wellKnownApi.getWellKnownVersion()
    .catch(() => null);

  version = version?.replace('-staging', '') ?? null;

  const isStaging = version?.includes('staging');
  const isDebug = version?.includes('debug');

  if (!isStaging && !isDebug) {
    // pieces os needs to update
    if (version && semver.lt(version, minimumVersion)) {
      document.getElementById('gpt-tab')?.classList.remove('!hidden');
      document.getElementById('pieces-copilot')?.classList.add('!hidden');
      if (semver.lt(version, '9.0.2'))
        // pieces os does not have auto update capabilities previously 9.0.2
        showErorrView('Please Update Pieces OS!');
      else await PiecesOSUpdating.getInstance().performUpdate();
    }
    // extension needs to update
    if (version && semver.gte(version, maximumVersion)) {
      document.getElementById('gpt-tab')?.classList.remove('!hidden');
      document.getElementById('pieces-copilot')?.classList.add('!hidden');
      showErorrView(
        `The Pieces for VS Code extension needs to be updated in order to work with Pieces OS version >= ${maximumVersion}`
      );
    }
  }

  if (!connected) {
    document.getElementById('pieces-copilot')?.classList.add('!hidden');
    if (!document.getElementById('copilot-error-view'))
      showErorrView('Pieces OS is not running!');
  } else if (
    document.getElementById('pieces-copilot')?.classList.contains('!hidden')
  ) {
    document.getElementById('copilot-error-view')?.remove();
    document.getElementById('pieces-copilot')?.classList.remove('!hidden');
    setIframeUrl();
  }

  await new Promise((res) => setTimeout(res, 5000));
  return connectionPoller();
}

async function getCopilotUrl() {
  const application = await copilotParams.getApplication();
  const baseUrl = await ConnectorSingleton.getInstance().osApi.osAppletLaunch({
    inactiveOSServerApplet: {
      type: OSAppletEnum.Copilot,
      parent: application,
    },
  });

  const url = new URL(`http://localhost:${baseUrl.port}`);

  const theme = getTheme();

  url.searchParams.append('theme', JSON.stringify(theme));
  url.searchParams.append('application', JSON.stringify(application));
  url.searchParams.append(
    'capabilities',
    (
      CopilotCapabilities.insertAtCursor |
      CopilotCapabilities.askCopilot |
      CopilotCapabilities.displayNotification |
      CopilotCapabilities.persistState |
      CopilotCapabilities.launchPos |
      CopilotCapabilities.setTheme |
      CopilotCapabilities.addToContext |
      CopilotCapabilities.copyToClipboard |
      CopilotCapabilities.loaded |
      CopilotCapabilities.previewAsset |
      CopilotCapabilities.openSettings
    ).toString()
  );
  if (copilotState) url.searchParams.append('state', copilotState);

  return url;
}

window.addEventListener('message', handleMessage);
