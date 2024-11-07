import { UpdatingStatusEnum } from '@pieces.app/pieces-os-client';
import ConnectorSingleton from '../../../connection/connector_singleton';
import { emptyEl, createDiv } from './globals';

export default class PiecesOSUpdating {
  private static instance: PiecesOSUpdating;

  private constructor() {
    //
  }

  /**
   * This will render the 'Pieces OS is updating' ui & update pieces os
   * @returns a promise which is resolved after timing out, or after pieces os has successfully been updated
   */
  public async performUpdate(): Promise<boolean> {
    const container = document.getElementById(
      'gpt-tab'
    ) as HTMLDivElement | null;
    if (!container) throw new Error('gpt-tab id is missing');
    emptyEl(container);
    container.classList.add(
      'w-full',
      'h-full',
      'flex',
      'flex-col',
      'py-10',
      'justify-center',
      'items-center',
      'bg-[var(--background-primary)]',
      'text-center',
      'text-[var(--text-muted)]',
      'px-4',
      'gap-2'
    );

    const titleEl = createDiv(container);
    titleEl.classList.add('px-2', 'text-lg', 'font-bold');
    titleEl.innerText = 'Pieces OS is Updating!';

    const expText = createDiv(container);
    expText.classList.add('px-2', 'font-semibold', 'break-words');
    expText.innerHTML =
      'Please wait while the latest version of Pieces OS is downloaded and installed! This should only take a few minutes.';

    const statusEl = createDiv(container);
    statusEl.classList.add('font-bold');
    statusEl.innerText = 'Checking for updates...';

    const progressContainer = createDiv(container);
    progressContainer.classList.add('w-1/2', 'self-center');

    let resolve: (val: boolean) => void;
    const ret = new Promise<boolean>((res) => {
      resolve = res;
    });
    // let timeoutId: NodeJS.Timeout;
    const intervalId = setInterval(async () => {
      const status = await ConnectorSingleton.getInstance()
        .osApi.osUpdateCheck({ uncheckedOSServerUpdate: {} })
        .catch(() => {
          return null;
        });
      statusEl.innerText = this.getStatusText(status?.status);
      if (status?.status === UpdatingStatusEnum.ReadyToRestart) {
        clearInterval(intervalId);
        statusEl.innerText = 'Restarting to apply the update';
        ConnectorSingleton.getInstance().osApi.osRestart();
        this.pollForConnection(resolve);
      }
    }, 3e3);
    // timeoutId =
    setTimeout(() => {
      clearInterval(intervalId);
      resolve(false);
    }, 10 * 60 * 1000); // after 10 minutes we will exit this task forcefully
    return ret;
  }

  /**
   * This will poll for a connection to pieces os (after the connection is lost due to restarting)
   * & resolve the updater promise when it has found a connection
   * if it doesn't find a connection after 5 minutes it will cancel the task
   * @param resolver the function to resolve the updater promise
   * @param removeMouseMoveListener function to remove the mouse move listener from the svg
   */
  private async pollForConnection(resolver: (val: boolean) => void) {
    let timeoutId: NodeJS.Timeout | undefined = undefined;
    const intervalId = setInterval(async () => {
      const connected = await ConnectorSingleton.getInstance()
        .wellKnownApi.getWellKnownHealth()
        .then(() => true)
        .catch(() => false);
      if (connected) {
        clearInterval(intervalId);
        resolver(true);
        clearTimeout(timeoutId);
      }
    }, 500);

    timeoutId = setTimeout(() => {
      clearInterval(intervalId);
      resolver(false);
    }, 5 * 60 * 1000); // after 5 minutes we will fail this task
  }

  /**
   * This converts UpdatingStatusEnum to a more user friendly format
   * @param status the status from the os update check endpoint
   * @returns readable text to represent the status
   */
  private getStatusText(status: UpdatingStatusEnum | undefined) {
    switch (status) {
      case UpdatingStatusEnum.Available:
        return 'Update detected...';
      case UpdatingStatusEnum.ContactSupport:
        return 'Something went wrong. Please contact support at https://docs.pieces.app/support';
      case UpdatingStatusEnum.Downloading:
        return 'Update is downloading...';
      case UpdatingStatusEnum.ReadyToRestart:
        return 'Restarting to apply the update...';
      case UpdatingStatusEnum.ReinstallRequired:
        return 'You need to reinstall Pieces OS for this feature to work!';
      case UpdatingStatusEnum.Unknown:
        return 'Unknown status';
      case UpdatingStatusEnum.UpToDate:
        return 'Pieces OS is up to date.';
      case undefined:
        return 'Failed to get update status, please contact support at https://docs.pieces.app/support';
    }
  }

  public static getInstance() {
    return (this.instance ??= new PiecesOSUpdating());
  }
}
