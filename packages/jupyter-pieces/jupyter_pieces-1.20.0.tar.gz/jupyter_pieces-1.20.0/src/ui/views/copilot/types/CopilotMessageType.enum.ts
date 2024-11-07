export enum CopilotWebviewMessageEnum {
  OpenFile = 'openFile',
  ShareReq = 'shareReq',
  Notify = 'notify',
  LoadContext = 'loadContext',
  ApplicationReq = 'applicationReq',
  OpenLink = 'openLink',
  Track = 'track',
  AddAssetToContext = 'addAssetToContext',
  AddFileToContext = 'addFileToContext',
  AddFolderToContext = 'addFolderToContext',
  FilterFolderReq = 'filterFolderReq',
  InsertAtCursor = 'insertAtCursor',
  RunInTerminal = 'runInTerminal',
  GetRecentFilesReq = 'getRecentFilesReq',
  GetWorkspacePathReq = 'getWorkspacePathReq',
  AcceptChanges = 'acceptChanges',
  CorsProxyReq = 'corsProxyReq',
  UpdateApplicationReq = 'updateApplicationReq',
  GetStateReq = 'getStateReq',
  SetStateReq = 'setStateReq',
}

export enum CopilotExtensionMessageEnum {
  ShareRes = 'shareRes',
  PerformQuery = 'performQuery',
  ApplicationRes = 'applicationRes',
  FilterFolderRes = 'filterFolderRes',
  GetRecentFilesRes = 'getRecentFilesRes',
  GetWorkSpacePathRes = 'getWorkspacePathRes',
  CorsProxyRes = 'corsProxyRes',
  UpdateApplicationRes = 'updateApplicationRes',
  GetStateRes = 'getStateRes',
}

export type ExtensionMsgExcludeUniEnum = Exclude<
  CopilotExtensionMessageEnum,
  'performQuery'
>;
export type WebviewMsgExcludeUniEnum = Exclude<
  CopilotWebviewMessageEnum,
  | 'notify'
  | 'openFile'
  | 'loadContext'
  | 'downloadModel'
  | 'openLink'
  | 'cancelDownload'
  | 'track'
  | 'addAssetToContext'
  | 'addFolderToContext'
  | 'addFileToContext'
  | 'runInTerminal'
  | 'insertAtCursor'
  | 'acceptChanges'
  | 'setStateReq'
>;
