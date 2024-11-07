import { CopilotDataTypes } from './CopilotMessageDataTypes';
import { CopilotWebviewMessageEnum } from './CopilotMessageType.enum';

export type CopilotReqToResponse = {
  [CopilotWebviewMessageEnum.ShareReq]: CopilotDataTypes['shareRes'];
  [CopilotWebviewMessageEnum.ApplicationReq]: CopilotDataTypes['applicationRes'];
  [CopilotWebviewMessageEnum.FilterFolderReq]: CopilotDataTypes['filterFolderRes'];
  [CopilotWebviewMessageEnum.GetRecentFilesReq]: CopilotDataTypes['getRecentFilesRes'];
  [CopilotWebviewMessageEnum.GetWorkspacePathReq]: CopilotDataTypes['getWorkspacePathRes'];
  [CopilotWebviewMessageEnum.CorsProxyReq]: CopilotDataTypes['corsProxyRes'];
  [CopilotWebviewMessageEnum.UpdateApplicationReq]: CopilotDataTypes['updateApplicationRes'];
  [CopilotWebviewMessageEnum.GetStateReq]: CopilotDataTypes['getStateRes'];
};
