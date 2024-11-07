import { CopilotState } from './ConversationState';
import { CopilotUnidirectionalMessage } from './CopilotUnidirectionalMessageData';

type CopilotViewParams =
  | {
      query: CopilotUnidirectionalMessage['performQuery'] & {
        conversationId: string;
      };
      state?: undefined; // enforce that this should not be passed with a query without breaking existing typing
    }
  | {
      state: CopilotState & {
        relevant?: CopilotUnidirectionalMessage['performQuery']['relevant'];
        replaceable?: CopilotUnidirectionalMessage['performQuery']['replaceable'];
      };
      query?: undefined; // enforce that this should not be passed with a state without breaking existing typing
    }
  | Record<string, never>; // type for empty object
