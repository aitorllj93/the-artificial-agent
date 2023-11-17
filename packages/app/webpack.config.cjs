const { composePlugins, withNx } = require('@nrwl/webpack');
const nodeExternals = require('webpack-node-externals');

// Nx plugins for webpack.
module.exports = async (config, ctx) => {
  return composePlugins(withNx(), (config) => {
    // Update the webpack config as needed here.
    // e.g. `config.plugins.push(new MyPlugin())`

    return {
      ...config,
      externalsPresets: {
        node: true,
      },
      output: {
        ...config.output,
        module: true,
        libraryTarget: 'module',
        chunkFormat: 'module',
        library: {
          type: 'module',
        },
        environment: {
          module: true,
        },
      },
      experiments: {
        ...config.experiments,
        outputModule: true,
        topLevelAwait: true,
      },
      externals: nodeExternals({
        importType: 'module',
      }),
    };
  })(config, ctx);
};
