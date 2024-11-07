import { ClassificationSpecificEnum } from 'core_openapi';

export type CopilotAssetSeed = {
	text: string;
	extension?: ClassificationSpecificEnum;
	filePath?: string;
};
