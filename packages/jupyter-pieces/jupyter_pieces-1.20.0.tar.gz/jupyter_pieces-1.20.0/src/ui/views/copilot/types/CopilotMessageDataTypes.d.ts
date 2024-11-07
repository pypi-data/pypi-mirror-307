/* eslint-disable no-mixed-spaces-and-tabs */
import { Application } from 'core_openapi';

/**
 * Declares all valid data types for message communication between Copilot webview and the backend extension
 */
/**
 * Declares all valid data types for message communication between Copilot webview and the backend extension
 */
export type CopilotDataTypes = {
	shareReq:
		| {
				asset: {
					raw: string;
					ext: string;
				};
		  }
		| {
				id: string;
		  };
	shareRes: { link: string | undefined; id: string };
	applicationReq: undefined;
	applicationRes: Application | undefined;
	filterFolderReq: string[];
	filterFolderRes: string[];
	getRecentFilesReq: undefined;
	getRecentFilesRes: { paths: string[] };
	getWorkspacePathReq: undefined;
	getWorkspacePathRes: { paths: string[] };
	corsProxyReq: { url: string; options?: RequestInit };
	corsProxyRes: { content: string };
	updateApplicationReq: { application: Application };
	updateApplicationRes: undefined;
	getStateReq: undefined;
	getStateRes: { state: string };
};
