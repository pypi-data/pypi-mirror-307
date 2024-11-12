import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @stellars/jupyterlab_darcula_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@stellars/jupyterlab_darcula_theme:plugin',
  description: 'IntelliJ Darcula Theme tweaked by Stellars, based on original Darcula theme',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @stellars/jupyterlab_darcula_theme is activated!');
    const style = '@stellars/jupyterlab_darcula_theme/index.css';

    manager.register({
      name: 'Stellars Darcula',
      themeScrollbars: true,
      isLight: false,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
