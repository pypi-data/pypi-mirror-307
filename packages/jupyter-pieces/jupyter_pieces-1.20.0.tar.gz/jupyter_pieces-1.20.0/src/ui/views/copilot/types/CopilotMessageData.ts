/* eslint-disable no-mixed-spaces-and-tabs */
import {
  CopilotExtensionMessageEnum,
  CopilotWebviewMessageEnum,
} from './CopilotMessageType.enum';
import { CopilotDataTypes } from './CopilotMessageDataTypes';
import { CopilotUnidirectionalMessage } from './CopilotUnidirectionalMessageData';

export type BaseCopilotMessage<
  T extends CopilotExtensionMessageEnum | CopilotWebviewMessageEnum,
> = { type: T; id: string; error?: string };

/**
 *  For one directional message we don't need an id or an error
 */
export type BaseUnidirectionalCopilotMessage<
  T extends CopilotExtensionMessageEnum | CopilotWebviewMessageEnum,
> = {
  type: T;
  error?: string;
};

/**
 * Declares all valid types of messages to be sent
 * @param T: the type of message to be sent/received
 */
export type CopilotMessageData<
  T extends CopilotWebviewMessageEnum | CopilotExtensionMessageEnum,
> = T extends keyof CopilotUnidirectionalMessage
  ? BaseUnidirectionalCopilotMessage<T> & {
      data: CopilotUnidirectionalMessage[T];
    }
  : T extends keyof CopilotDataTypes
  ? BaseCopilotMessage<T> & { data: CopilotDataTypes[T] }
  : BaseCopilotMessage<T>;
