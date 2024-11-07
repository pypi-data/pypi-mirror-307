import { QGPTPromptPipeline } from 'core_openapi';
import { CopilotAnalytics } from './CopilotAnalytics.enum';
import { CopilotAssetSeed } from './EditorSeed';
import { NotificationParameters } from './NotificationParameters';
import { CopilotRange } from './range';

/**
 * These messages only go one way, front end -> backend or backend -> front end
 */

export type AskAboutFileInput = { paths: string[]; parent: string };
export type CopilotUnidirectionalMessage = {
	performQuery: {
		query: string;
		relevant?: CopilotAssetSeed;
		files?: AskAboutFileInput;
		snippet?: { id: string };
		replaceable?: {
			rangeToReplace: CopilotRange;
			filePath: string;
		};
		pipeline?: QGPTPromptPipeline;
	};
	openFile: { path: string };
	notify: { params: NotificationParameters };
	track: CopilotAnalytics; // TODO implement tracking
	loadContext: { paths: string[] };
	downloadModel: { id: string };
	openLink: { link: string };
	cancelDownload: { id: string };
	addAssetToContext: { conversation: string };
	addFileToContext: { conversation: string };
	addFolderToContext: { conversation: string };
	runInTerminal: { command: string };
	insertAtCursor: { text: string };
	acceptChanges: {
		rangeToReplace: CopilotRange;
		filePath: string;
		replacement: string;
	};
	setStateReq: {
		state: string;
	};
};
