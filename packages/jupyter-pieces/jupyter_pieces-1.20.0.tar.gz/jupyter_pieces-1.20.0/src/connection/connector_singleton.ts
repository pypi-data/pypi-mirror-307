import {
  AnchorsApi,
  ApplicationNameEnum,
  ApplicationsApi,
  CapabilitiesEnum,
  Configuration,
  ConfigurationParameters,
  ConnectorApi,
  Context,
  ConversationApi,
  PlatformEnum,
  SeededConnectorConnection,
  SeededConnectorTracking,
  SeededTrackedApplication,
  TrackRequest,
} from '@pieces.app/pieces-os-client';
import {
  AllocationsApi,
  ApplicationApi,
  AssetApi,
  AssetsApi,
  Configuration as CoreConfig,
  FormatApi,
  LinkifyApi,
  SearchApi,
  OSApi,
  UserApi,
  WellKnownApi,
  DiscoveryApi,
  QGPTApi,
  AnnotationApi,
  AnnotationsApi,
  ActivityApi,
  ActivitiesApi,
  ModelApi,
  ModelsApi,
} from '@pieces.app/pieces-os-client';
import Notifications from './notification_handler';
import Constants from '../const';
import { getStored } from '../localStorageManager';

export const portNumber = getStored('Port')
  ? getStored('Port')
  : navigator.userAgent.toLowerCase().includes('linux')
  ? 5323
  : 1000;

export default class ConnectorSingleton {
  private static instance: ConnectorSingleton;
  private _platform = process.platform;
  private _platformMap: { [key: string]: PlatformEnum } = {
    win32: PlatformEnum.Windows,
    darwin: PlatformEnum.Macos,
    linux: PlatformEnum.Linux,
  };

  private constructor() {
    this.createApis();
  }

  public parameters: ConfigurationParameters = {
    basePath: `http://localhost:${portNumber}`,
    fetchApi: fetch,
  };

  public context!: Context;
  public configuration: Configuration = new Configuration(this.parameters);
  public api!: ConnectorApi;
  public conversationApi!: ConversationApi;
  public anchorsApi!: AnchorsApi;
  public modelApi!: ModelApi;
  public modelsApi!: ModelsApi;
  public searchApi!: SearchApi;
  public allocationsApi!: AllocationsApi;
  public applicationApi!: ApplicationApi;
  public applicationsApi!: ApplicationsApi;
  public linkifyApi!: LinkifyApi;
  public assetsApi!: AssetsApi;
  public formatApi!: FormatApi;
  public userApi!: UserApi;
  public osApi!: OSApi;
  public assetApi!: AssetApi;
  public DiscoveryApi!: DiscoveryApi;
  public wellKnownApi!: WellKnownApi;
  public QGPTApi!: QGPTApi;
  public annotationsApi!: AnnotationsApi;
  public annotationApi!: AnnotationApi;
  public activityApi!: ActivityApi;
  public activitiesApi!: ActivitiesApi;

  addHeader(application: string) {
    this.createApis(application);
  }

  private createApis(application?: string) {
    if (application) {
      (this.parameters.headers ??= {})['application'] = application;
    }

    this.configuration = new Configuration(this.parameters);

    const coreConfig = new CoreConfig({
      fetchApi: fetch,
      basePath: this.parameters.basePath,
      headers: this.parameters.headers,
    });

    this.api = new ConnectorApi(this.configuration);
    this.conversationApi = new ConversationApi(coreConfig);
    this.anchorsApi = new AnchorsApi(coreConfig);
    this.modelApi = new ModelApi(coreConfig);
    this.modelsApi = new ModelsApi(coreConfig);
    this.searchApi = new SearchApi(coreConfig);
    this.allocationsApi = new AllocationsApi(coreConfig);
    this.applicationApi = new ApplicationApi(coreConfig);
    this.applicationsApi = new ApplicationsApi(coreConfig);
    this.linkifyApi = new LinkifyApi(coreConfig);
    this.assetsApi = new AssetsApi(coreConfig);
    this.formatApi = new FormatApi(coreConfig);
    this.userApi = new UserApi(coreConfig);
    this.osApi = new OSApi(coreConfig);
    this.assetApi = new AssetApi(coreConfig);
    this.DiscoveryApi = new DiscoveryApi(coreConfig);
    this.wellKnownApi = new WellKnownApi(coreConfig);
    this.QGPTApi = new QGPTApi(coreConfig);
    this.annotationsApi = new AnnotationsApi(coreConfig);
    this.annotationApi = new AnnotationApi(coreConfig);
    this.activityApi = new ActivityApi(coreConfig);
    this.activitiesApi = new ActivitiesApi(coreConfig);
  }

  public application: SeededTrackedApplication = {
    name: ApplicationNameEnum.JupyterHub,
    version: Constants.PLUGIN_VERSION,
    platform: this._platformMap[this._platform] || PlatformEnum.Unknown,
    capabilities: getStored('Capabilities')
      ? getStored('Capabilities')
      : CapabilitiesEnum.Blended,
  };

  public seeded: SeededConnectorConnection = {
    application: this.application,
  };

  public static getInstance(): ConnectorSingleton {
    if (!ConnectorSingleton.instance) {
      ConnectorSingleton.instance = new ConnectorSingleton();
    }

    return ConnectorSingleton.instance;
  }

  public static async checkConnection({
    notification = true,
  }: {
    notification?: boolean;
  }): Promise<boolean> {
    try {
      await fetch(`http://localhost:${portNumber}/.well-known/health`);
      return true;
    } catch (e) {
      const notifications = Notifications.getInstance();
      // if notification is set to false we will ignore and just return false.
      if (notification) {
        notifications.information({
          message: Constants.CORE_PLATFORM_MSG,
        });
      }
      return false;
    }
  }

  public async track(event: SeededConnectorTracking): Promise<boolean> {
    const { context, api } = this;

    if (!context) {
      throw new Error('Application context could not be found when calling');
    }

    const seededConnectorTracking: SeededConnectorTracking = { ...event };

    const seed: TrackRequest = {
      application: context.application.id,
      seededConnectorTracking,
    };
    return api
      .track(seed)
      .then((_) => true)
      .catch((error) => {
        // TODO send this to sentry. and extract the actual error from the error.(ie error.message)
        console.log(`Error from api.track Error: ${error}`);
        return false;
      });
  }
}
