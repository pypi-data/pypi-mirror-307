import { QGPTQuestionOutput, RelevantQGPTSeed } from 'core_openapi';
import { AskAboutFileInput } from './CopilotUnidirectionalMessageData';
import { QGPTConversationMessage } from 'core_openapi';
import { Directive } from './Directive';
import { CopilotColors } from './Colors';

type ConversationObject = {
	message: QGPTConversationMessage;
	relevant?: RelevantQGPTSeed[];
	files?: AskAboutFileInput;
	image: boolean;
	messageId: string;
};

export type CopilotState = {
	conversation: ConversationObject[];
	conversationId: string;
	hints?: QGPTQuestionOutput;
	selectedModel: string;
	migration: number;
	directives: Directive[];
	colors?: CopilotColors;
	highContrast?: boolean;
};
