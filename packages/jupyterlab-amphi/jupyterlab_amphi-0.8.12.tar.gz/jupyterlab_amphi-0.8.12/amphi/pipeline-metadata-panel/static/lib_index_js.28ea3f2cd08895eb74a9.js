"use strict";
(self["webpackChunk_amphi_pipeline_metadata_panel"] = self["webpackChunk_amphi_pipeline_metadata_panel"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DummyHandler: () => (/* binding */ DummyHandler),
/* harmony export */   VariableInspectionHandler: () => (/* binding */ VariableInspectionHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__);


class AbstractHandler {
    constructor(connector) {
        this._isDisposed = false;
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._rendermime = null;
        this._connector = connector;
    }
    get disposed() {
        return this._disposed;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    get inspected() {
        return this._inspected;
    }
    get rendermime() {
        return this._rendermime;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    performDelete(varName) {
        //noop
    }
    performAllDelete() {
        //noop
    }
}
/**
 * An object that handles code inspection.
 */
class VariableInspectionHandler extends AbstractHandler {
    constructor(options) {
        var _a;
        super(options.connector);
        this._inspectionChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        /*
         * Handle query response. Emit new signal containing the IMetadataPanel.IInspectorUpdate object.
         * (TODO: query resp. could be forwarded to panel directly)
         */
        this._handleQueryResponse = (response) => {
            const msgType = response.header.msg_type;
            switch (msgType) {
                case 'execute_result': {
                    const payload = response.content;
                    let sample = payload.data['text/html'];
                    let content = payload.data['text/plain'];
                    if (content.slice(0, 1) === "'" || content.slice(0, 1) === '"') {
                        content = content.slice(1, -1);
                        content = content.replace(/\\"/g, '"').replace(/\\'/g, "'");
                    }
                    this._inspectionChanged.emit(content); // Emit signal with payload
                    const update = JSON.parse(content);
                    const title = {
                        contextName: '',
                        kernelName: this._connector.kernelName || ''
                    };
                    this._inspected.emit({ title: title, payload: update });
                    break;
                }
                case 'display_data': {
                    const payloadDisplay = response.content;
                    let contentDisplay = payloadDisplay.data['text/plain'];
                    if (contentDisplay.slice(0, 1) === "'" ||
                        contentDisplay.slice(0, 1) === '"') {
                        contentDisplay = contentDisplay.slice(1, -1);
                        contentDisplay = contentDisplay
                            .replace(/\\"/g, '"')
                            .replace(/\\'/g, "'");
                    }
                    const updateDisplay = JSON.parse(contentDisplay);
                    const titleDisplay = {
                        contextName: '',
                        kernelName: this._connector.kernelName || ''
                    };
                    this._inspected.emit({ title: titleDisplay, payload: updateDisplay });
                    break;
                }
                default:
                    break;
            }
        };
        /*
         * Invokes a inspection if the signal emitted from specified session is an 'execute_input' msg.
         */
        this._queryCall = (sess, msg) => {
            const msgType = msg.header.msg_type;
            switch (msgType) {
                case 'execute_input': {
                    const code = msg.content.code;
                    if (!(code === this._queryCommand) &&
                        !(code === this._matrixQueryCommand) &&
                        !code.startsWith(this._widgetQueryCommand)) {
                        this.performInspection();
                    }
                    break;
                }
                default:
                    break;
            }
        };
        this._id = options.id;
        this._rendermime = (_a = options.rendermime) !== null && _a !== void 0 ? _a : null;
        this._queryCommand = options.queryCommand;
        this._matrixQueryCommand = options.matrixQueryCommand;
        this._widgetQueryCommand = options.widgetQueryCommand;
        this._deleteCommand = options.deleteCommand;
        this._deleteAllCommand = options.deleteAllCommand;
        this._initScript = options.initScript;
        this._ready = this._connector.ready.then(() => {
            this._initOnKernel().then((msg) => {
                this._connector.iopubMessage.connect(this._queryCall);
                return;
            });
        });
        this._connector.kernelRestarted.connect((sender, kernelReady) => {
            const title = {
                contextName: '<b>Restarting kernel...</b> '
            };
            this._inspected.emit({
                title: title,
                payload: []
            });
            this._ready = kernelReady.then(() => {
                this._initOnKernel().then((msg) => {
                    this._connector.iopubMessage.connect(this._queryCall);
                    // this.performInspection();
                });
            });
        });
    }
    get id() {
        return this._id;
    }
    get ready() {
        return this._ready;
    }
    /**
     * Performs an inspection by sending an execute request with the query command to the kernel.
     */
    performInspection() {
        const content = {
            code: this._queryCommand,
            stop_on_error: false,
            store_history: false
        };
        this._connector.fetch(content, this._handleQueryResponse);
    }
    /**
     * Performs an inspection of a Jupyter Widget
     */
    performWidgetInspection(varName) {
        const request = {
            code: this._widgetQueryCommand + '(' + varName + ')',
            stop_on_error: false,
            store_history: false
        };
        return this._connector.execute(request);
    }
    /**
     * Performs an inspection of the specified matrix.
     */
    performMatrixInspection(varName, maxRows = 10000) {
        const request = {
            code: this._matrixQueryCommand + '(' + varName + ', ' + maxRows + ')',
            stop_on_error: false,
            store_history: false
        };
        const con = this._connector;
        return new Promise((resolve, reject) => {
            con.fetch(request, (response) => {
                const msgType = response.header.msg_type;
                switch (msgType) {
                    case 'execute_result': {
                        const payload = response.content;
                        let content = payload.data['text/plain'];
                        content = content.replace(/^'|'$/g, '');
                        content = content.replace(/\\"/g, '"');
                        content = content.replace(/\\'/g, "\\\\'");
                        const modelOptions = JSON.parse(content);
                        const jsonModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.JSONModel(modelOptions);
                        resolve(jsonModel);
                        break;
                    }
                    case 'error':
                        reject("Kernel error on 'matrixQuery' call!");
                        break;
                    default:
                        break;
                }
            });
        });
    }
    /*
      if (args.msg.header.msg_type === 'execute_result' || args.msg.header.msg_type === 'display_data') {
        // Assert the message type to IExecuteResultMsg or IDisplayDataMsg to access 'data'
        const content = args.msg.content as KernelMessage.IExecuteResultMsg['content'] | KernelMessage.IDisplayDataMsg['content'];
        if (content.data['text/html']) {
          // Now 'content.data' is properly recognized by TypeScript
          const htmlData = content.data['text/html'];
          // Handle the HTML data
          manager.panel.onNewLog(formatLogDate(args.msg.header.date), "info", htmlData)
        }
      }
      */
    /**
     * Performs an inspection of the specified matrix.
     */
    performPreview(varName) {
        const request = {
            code: varName,
            stop_on_error: false,
            store_history: false
        };
        const con = this._connector;
        return new Promise((resolve, reject) => {
            con.fetch(request, (response) => {
                const msgType = response.header.msg_type;
                switch (msgType) {
                    case 'execute_result': {
                        const content = response.content;
                        if (content.data['text/html']) {
                            // Now 'content.data' is properly recognized by TypeScript
                            const htmlData = content.data['text/html'];
                            // Handle the HTML data
                            resolve(htmlData);
                        }
                        break;
                    }
                    case 'error':
                        reject("Kernel error on 'preview query' call!");
                        break;
                    default:
                        break;
                }
            });
        });
    }
    /**
     * Send a kernel request to delete a variable from the global environment
     */
    performDelete(varName) {
        const content = {
            code: this._deleteCommand + "('" + varName + "')",
            stop_on_error: false,
            store_history: false
        };
        this._connector.fetch(content, this._handleQueryResponse);
    }
    /**
     * Send a kernel request to delete all variables from the global environment
     */
    performAllDelete() {
        const content = {
            code: this._deleteAllCommand + "()",
            stop_on_error: false,
            store_history: false
        };
        this._connector.fetch(content, this._handleQueryResponse);
    }
    /**
     * Initializes the kernel by running the set up script located at _initScriptPath.
     */
    _initOnKernel() {
        const content = {
            code: this._initScript,
            stop_on_error: false,
            silent: true
        };
        return this._connector.fetch(content, () => {
            //no op
        });
    }
}
class DummyHandler extends AbstractHandler {
    constructor(connector) {
        super(connector);
    }
    performInspection() {
        const title = {
            contextName: '. <b>Language currently not supported.</b> ',
            kernelName: this._connector.kernelName || ''
        };
        this._inspected.emit({
            title: title,
            payload: []
        });
    }
    performMatrixInspection(varName, maxRows) {
        return new Promise((resolve, reject) => {
            reject('Cannot inspect matrices w/ the DummyHandler!');
        });
    }
    performPreview(varName) {
        return new Promise((resolve, reject) => {
            reject('Cannot preview df w/ the DummyHandler!');
        });
    }
    performWidgetInspection(varName) {
        const request = {
            code: '',
            stop_on_error: false,
            store_history: false
        };
        return this._connector.execute(request);
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VariableInspectionHandler: () => (/* reexport safe */ _handler__WEBPACK_IMPORTED_MODULE_6__.VariableInspectionHandler),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @amphi/pipeline-editor */ "webpack/sharing/consume/default/@amphi/pipeline-editor");
/* harmony import */ var _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _inspectorscripts__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./inspectorscripts */ "./lib/inspectorscripts.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./kernelconnector */ "./lib/kernelconnector.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");
/* harmony import */ var _metadatapanel__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./metadatapanel */ "./lib/metadatapanel.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);













var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'metadatapanel:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing variable introspection.
 */
const metadatapanel = {
    id: '@amphi/pipeline-metadata-panel',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_7__.IMetadataPanelManager,
    autoStart: true,
    activate: (app, palette, restorer, labShell, settings) => {
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_8__.MetadataPanelManager();
        const category = 'Metadata Panel';
        const command = CommandIDs.open;
        const label = 'Open Metadata Panel';
        const namespace = 'metadatapanel';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({ namespace });
        /**
         * Create and track a new inspector.
         */
        function newPanel() {
            const panel = new _metadatapanel__WEBPACK_IMPORTED_MODULE_9__.MetadataPanelPanel(app);
            panel.id = 'amphi-metadataPanel';
            panel.title.label = 'Metadata Panel';
            panel.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.inspectorIcon;
            panel.title.closable = true;
            panel.disposed.connect(() => {
                if (manager.panel === panel) {
                    manager.panel = null;
                }
            });
            //Track the inspector panel
            tracker.add(panel);
            return panel;
        }
        // Add command to palette
        app.commands.addCommand(command, {
            label,
            execute: () => {
                const logConsoleId = 'amphi-logConsole'; // Using the provided log console panel ID
                let logConsolePanel = null;
                // Iterate over each widget in the 'main' area to find the log console
                for (const widget of app.shell.widgets('main')) {
                    if (widget.id === logConsoleId) {
                        logConsolePanel = widget;
                        break;
                    }
                }
                if (!manager.panel || manager.panel.isDisposed) {
                    manager.panel = newPanel();
                }
                // Check if the log console panel is found and is attached
                if (logConsolePanel && logConsolePanel.isAttached) {
                    // If log console panel is open, add the preview panel as a tab next to it
                    if (!manager.panel.isAttached) {
                        app.shell.add(manager.panel, 'main', { ref: logConsolePanel.id, mode: 'tab-after' });
                    }
                }
                else {
                    // If log console panel is not open, open the preview panel in split-bottom mode
                    if (!manager.panel.isAttached) {
                        app.shell.add(manager.panel, 'main', { mode: 'split-bottom' });
                    }
                }
                if (manager.source) {
                    manager.source.performInspection();
                }
                app.shell.activateById(manager.panel.id);
            }
        });
        palette.addItem({ command, category });
        // Add command to palette
        app.commands.addCommand('pipeline-metadata-panel:delete-all', {
            label,
            execute: () => {
                if (manager.source) {
                    manager.source.performAllDelete();
                }
            }
        });
        // Enable state restoration
        restorer.restore(tracker, {
            command,
            args: () => ({}),
            name: () => 'metadatapanel'
        });
        console.log('JupyterLab extension @amphi/pipeline-metadata-panel is activated!');
        return manager;
    }
};
/**
 * An extension that registers Pipelines for variable inspection.
 */
const consoles = {
    id: '@amphi/pipeline-metadata-panel:consoles',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IMetadataPanelManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell) => {
        const handlers = {};
        /**
         * Subscribes to the creation of new consoles. If a new notebook is created, build a new handler for the consoles.
         * Adds a promise for a instanced handler to the 'handlers' collection.
         */
        consoles.widgetAdded.connect((sender, consolePanel) => {
            if (manager.hasHandler(consolePanel.sessionContext.path)) {
                handlers[consolePanel.id] = new Promise((resolve, reject) => {
                    resolve(manager.getHandler(consolePanel.sessionContext.path));
                });
            }
            else {
                handlers[consolePanel.id] = new Promise((resolve, reject) => {
                    const session = consolePanel.sessionContext;
                    // Create connector and init w script if it exists for kernel type.
                    const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_10__.KernelConnector({ session });
                    const scripts = connector.ready.then(() => {
                        return connector.kernelLanguage.then(lang => {
                            return _inspectorscripts__WEBPACK_IMPORTED_MODULE_11__.Languages.getScript(lang);
                        });
                    });
                    scripts.then((result) => {
                        const initScript = result.initScript;
                        const queryCommand = result.queryCommand;
                        const matrixQueryCommand = result.matrixQueryCommand;
                        const widgetQueryCommand = result.widgetQueryCommand;
                        const deleteCommand = result.deleteCommand;
                        const deleteAllCommand = result.deleteAllCommand;
                        const options = {
                            queryCommand: queryCommand,
                            matrixQueryCommand: matrixQueryCommand,
                            widgetQueryCommand,
                            deleteCommand: deleteCommand,
                            deleteAllCommand: deleteAllCommand,
                            connector: connector,
                            initScript: initScript,
                            id: session.path //Using the sessions path as an identifier for now.
                        };
                        const handler = new _handler__WEBPACK_IMPORTED_MODULE_6__.VariableInspectionHandler(options);
                        manager.addHandler(handler);
                        consolePanel.disposed.connect(() => {
                            delete handlers[consolePanel.id];
                            handler.dispose();
                        });
                        handler.ready.then(() => {
                            resolve(handler);
                        });
                    });
                    //Otherwise log error message.
                    scripts.catch((result) => {
                        const handler = new _handler__WEBPACK_IMPORTED_MODULE_6__.DummyHandler(connector);
                        consolePanel.disposed.connect(() => {
                            delete handlers[consolePanel.id];
                            handler.dispose();
                        });
                        resolve(handler);
                    });
                });
            }
            setSource(labShell);
        });
        const setSource = (sender, args) => {
            var _a;
            const widget = (_a = args === null || args === void 0 ? void 0 : args.newValue) !== null && _a !== void 0 ? _a : sender.currentWidget;
            if (!widget || !consoles.has(widget)) {
                return;
            }
            const future = handlers[widget.id];
            future.then((source) => {
                if (source) {
                    manager.source = source;
                    manager.source.performInspection();
                }
            });
        };
        /**
         * If focus window changes, checks whether new focus widget is a console.
         * In that case, retrieves the handler associated to the console after it has been
         * initialized and updates the manager with it.
         */
        setSource(labShell);
        labShell.currentChanged.connect(setSource);
        app.contextMenu.addItem({
            command: CommandIDs.open,
            selector: '.jp-CodeConsole'
        });
    }
};
/**
 * An extension that registers consoles for variable inspection.
 */
const pipelines = {
    id: '@amphi/pipeline-metadata-panel:pipelines',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IMetadataPanelManager, _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_4__.IPipelineTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    autoStart: true,
    activate: (app, manager, pipelines, labShell, settings) => {
        const handlers = {};
        let customCodeInitialization = "";
        function loadSetting(setting) {
            customCodeInitialization = setting.get('customCodeInitialization').composite;
            console.log(`Settings: Amphi Metadata extension: customCodeInitialization is set to '${customCodeInitialization}'`);
        }
        settings.load('@amphi/pipeline-metadata-panel:pipelines')
            .then((setting) => {
            // Initial call to loadSetting after the settings are first loaded
            loadSetting(setting);
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            /**
             * Subscribes to the creation of new pipelines. If a new notebook is created, build a new handler for the consoles.
             * Adds a promise for a instanced handler to the 'handlers' collection.
             */
            pipelines.widgetAdded.connect((sender, pipelinePanel) => {
                if (manager.hasHandler(pipelinePanel.context.sessionContext.path)) {
                    handlers[pipelinePanel.id] = new Promise((resolve, reject) => {
                        resolve(manager.getHandler(pipelinePanel.context.sessionContext.path));
                    });
                }
                else {
                    handlers[pipelinePanel.id] = new Promise((resolve, reject) => {
                        const session = pipelinePanel.context.sessionContext;
                        // Create connector and init w script if it exists for kernel type.
                        const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_10__.KernelConnector({ session });
                        const scripts = connector.ready.then(() => {
                            return connector.kernelLanguage.then(lang => {
                                return _inspectorscripts__WEBPACK_IMPORTED_MODULE_11__.Languages.getScript(lang);
                            });
                        });
                        scripts.then((result) => {
                            const initScript = result.initScript + "\n" + customCodeInitialization;
                            const queryCommand = result.queryCommand;
                            const matrixQueryCommand = result.matrixQueryCommand;
                            const widgetQueryCommand = result.widgetQueryCommand;
                            const deleteCommand = result.deleteCommand;
                            const deleteAllCommand = result.deleteAllCommand;
                            const options = {
                                queryCommand: queryCommand,
                                matrixQueryCommand: matrixQueryCommand,
                                widgetQueryCommand,
                                deleteCommand: deleteCommand,
                                deleteAllCommand: deleteAllCommand,
                                connector: connector,
                                initScript: initScript,
                                id: session.path //Using the sessions path as an identifier for now.
                            };
                            const handler = new _handler__WEBPACK_IMPORTED_MODULE_6__.VariableInspectionHandler(options);
                            manager.addHandler(handler);
                            pipelinePanel.disposed.connect(() => {
                                delete handlers[pipelinePanel.id];
                                handler.dispose();
                            });
                            handler.ready.then(() => {
                                resolve(handler);
                            });
                        });
                        //Otherwise log error message.
                        scripts.catch((result) => {
                            const handler = new _handler__WEBPACK_IMPORTED_MODULE_6__.DummyHandler(connector);
                            pipelinePanel.disposed.connect(() => {
                                delete handlers[pipelinePanel.id];
                                handler.dispose();
                            });
                            resolve(handler);
                        });
                    });
                }
                setSource(labShell);
            });
            const setSource = (sender, args) => {
                var _a;
                const widget = (_a = args === null || args === void 0 ? void 0 : args.newValue) !== null && _a !== void 0 ? _a : sender.currentWidget;
                if (!widget || !pipelines.has(widget)) {
                    return;
                }
                const future = handlers[widget.id];
                future.then((source) => {
                    if (source) {
                        manager.source = source;
                        manager.source.performInspection();
                    }
                });
            };
            /**
             * If focus window changes, checks whether new focus widget is a console.
             * In that case, retrieves the handler associated to the console after it has been
             * initialized and updates the manager with it.
             */
            setSource(labShell);
            labShell.currentChanged.connect(setSource);
        }).catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    metadatapanel,
    consoles,
    pipelines
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/inspectorscripts.js":
/*!*********************************!*\
  !*** ./lib/inspectorscripts.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Languages: () => (/* binding */ Languages)
/* harmony export */ });
class Languages {
    static getScript(lang) {
        return new Promise((resolve, reject) => {
            if (lang in Languages.scripts) {
                resolve(Languages.scripts[lang]);
            }
            else {
                reject('Language ' + lang + ' not supported yet!');
            }
        });
    }
}
/**
 * Init and query script for supported languages.
 */
Languages.py_script = `
import json
import sys
import types
import re
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

from importlib import __import__
from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics
from IPython.display import display, HTML

!pip install --quiet pandas==2.2.1 --disable-pip-version-check
!pip install --quiet sqlalchemy==2.0.4 --disable-pip-version-check
!pip install --quiet python-dotenv --disable-pip-version-check


_amphi_metadatapanel_nms = NamespaceMagics()
_amphi_metadatapanel_Jupyter = get_ipython()
# _amphi_metadatapanel_nms.shell = _amphi_metadatapanel_Jupyter.kernel.shell  
__np = None
__pd = None
__pl = None
__pyspark = None
__tf = None
__K = None
__torch = None
__ipywidgets = None
__xr = None
  
def _attempt_import(module):
    try:
        return __import__(module)
    except ImportError:
        return None


def _check_imported():
    global __np, __pd, __pyspark, __tf, __K, __torch, __ipywidgets, __xr

    __np = _attempt_import('numpy')
    __pd = _attempt_import('pandas')
    __pyspark = _attempt_import('pyspark')
    __tf = _attempt_import('tensorflow')
    __K = _attempt_import('keras.backend') or _attempt_import('tensorflow.keras.backend')
    __torch = _attempt_import('torch')
    __ipywidgets = _attempt_import('ipywidgets')
    __xr = _attempt_import('xarray')


def _amphi_metadatapanel_getsizeof(x):
    if type(x).__name__ in ['ndarray', 'Series']:
        return x.nbytes
    elif __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return "?"
    elif __tf and isinstance(x, __tf.Variable):
        return "?"
    elif __torch and isinstance(x, __torch.Tensor):
        return x.element_size() * x.nelement()
    elif __pd and type(x).__name__ == 'DataFrame':
        return x.memory_usage().sum()
    else:
        return sys.getsizeof(x)


def _amphi_metadatapanel_getshapeof(x):
    if __pd and isinstance(x, __pd.DataFrame):
        return "%d rows x %d cols" % x.shape
    if __pd and isinstance(x, __pd.Series):
        return "%d rows" % x.shape
    if __np and isinstance(x, __np.ndarray):
        shape = " x ".join([str(i) for i in x.shape])
        return "%s" % shape
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return "? rows x %d cols" % len(x.columns)
    if __tf and isinstance(x, __tf.Variable):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __tf and isinstance(x, __tf.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __torch and isinstance(x, __torch.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __xr and isinstance(x, __xr.DataArray):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if isinstance(x, list):
        return "%s" % len(x)
    if isinstance(x, dict):
        return "%s keys" % len(x)
    return None


def _amphi_metadatapanel_getcontentof(x):
    def check_unnamed_columns(df):
        # Consider columns with purely integer labels as unnamed, all others (including empty strings) as named
        unnamed_columns = [col for col in df.columns if isinstance(col, int)]
        return unnamed_columns

    # Check if the input is a Pandas DataFrame and handle it
    if __pd and isinstance(x, __pd.DataFrame):
        unnamed_cols = check_unnamed_columns(x)
        colnames = ', '.join([f"{col} ({dtype}, {'unnamed' if col in unnamed_cols else 'named'})" for col, dtype in zip(x.columns, x.dtypes)])
        content = "%s" % colnames

    # Check if the input is an Ibis Table and handle it similarly
    elif "ibis" in globals() and isinstance(x, ibis.expr.types.Table):
        schema = x.schema()
        colnames = ', '.join([f"{col} ({dtype}, named)" for col, dtype in schema.items()])
        content = "%s" % colnames

    # Handle other types accordingly
    elif __pd and isinstance(x, __pd.Series):
        content = f"{x.name} ({x.dtype}, {'unnamed' if x.name == '' or isinstance(x.name, int) else 'named'}), " + str(x.values).replace(" ", ", ")[1:-1]
        content = content.replace("\\n", "")
    elif __np and isinstance(x, __np.ndarray):
        content = f"ndarray (shape={x.shape}, dtype={x.dtype})"
    elif __xr and isinstance(x, __xr.DataArray):
        content = f"DataArray (shape={x.shape}, dtype={x.dtype})"
    else:
        content = f"{type(x).__name__}, " + str(x)

    return content


def _amphi_metadatapanel_is_matrix(x):
    # True if type(x).__name__ in ["DataFrame", "ndarray", "Series"] else False
    if __pd and isinstance(x, __pd.DataFrame):
        return True
    if __pd and isinstance(x, __pd.Series):
        return True
    if __np and isinstance(x, __np.ndarray) and len(x.shape) <= 2:
        return True
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return True
    if __tf and isinstance(x, __tf.Variable) and len(x.shape) <= 2:
        return True
    if __tf and isinstance(x, __tf.Tensor) and len(x.shape) <= 2:
        return True
    if __torch and isinstance(x, __torch.Tensor) and len(x.shape) <= 2:
        return True
    if __xr and isinstance(x, __xr.DataArray) and len(x.shape) <= 2:
        return True
    if isinstance(x, list):
        return True
    return False


def _amphi_metadatapanel_is_widget(x):
    return __ipywidgets and issubclass(x, __ipywidgets.DOMWidget)


def get_camel_case_variables():
    camel_case_pattern = re.compile(r'^[a-z]+(?:[A-Z][a-z]+)*(?:\\d+)?$')
    variable_names = []
    for key, value in globals().items():
        # Skip built-in, imported modules/objects, and certain IPython/Jupyter objects
        if not key.startswith('_') and not hasattr(__builtins__, key) and not key in ['exit', 'quit', 'get_ipython', 'In', 'Out'] and not isinstance(value, (type(sys), types.ModuleType)) and camel_case_pattern.match(key):
            variable_names.append(key)
    return variable_names

def _amphi_metadatapanel_dict_list():
    _check_imported()

    def keep_cond(obj):
        try:
            if isinstance(obj, str):
                return True
            if __tf and isinstance(obj, __tf.Variable):
                return True
            if __pd and __pd is not None and (
                isinstance(obj, __pd.core.frame.DataFrame)
                or isinstance(obj, __pd.core.series.Series)):
                return True
            if __xr and __xr is not None and isinstance(obj, __xr.DataArray):
                return True
            if str(obj)[0] == "<":
                return False
            return True
        except:
            return False

    camel_case_vars = get_camel_case_variables()
    vardic = [
        {
            'varName': var_name,
            'varType': type(eval(var_name)).__name__, 
            'varSize': str(_amphi_metadatapanel_getsizeof(eval(var_name))), 
            'varShape': str(_amphi_metadatapanel_getshapeof(eval(var_name))) if _amphi_metadatapanel_getshapeof(eval(var_name)) else '', 
            'varContent': str(_amphi_metadatapanel_getcontentof(eval(var_name))),
            'isMatrix': _amphi_metadatapanel_is_matrix(eval(var_name)),
            'isWidget': _amphi_metadatapanel_is_widget(type(eval(var_name)))
        }
        for var_name in camel_case_vars if keep_cond(eval(var_name))
    ]
    return json.dumps(vardic, ensure_ascii=False)
  
def _amphi_metadatapanel_getmatrixcontent(x, max_rows=10000):
    # to do: add something to handle this in the future
    threshold = max_rows

    if __pd and __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        df = x.limit(threshold).toPandas()
        return _amphi_metadatapanel_getmatrixcontent(df.copy())
    elif __np and __pd and type(x).__name__ == "DataFrame":
        if threshold is not None:
            x = x.head(threshold)
        x.columns = x.columns.map(str)
        return x.to_json(orient="table", default_handler=_amphi_metadatapanel_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "Series":
        if threshold is not None:
            x = x.head(threshold)
        return x.to_json(orient="table", default_handler=_amphi_metadatapanel_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "ndarray":
        df = __pd.DataFrame(x)
        return _amphi_metadatapanel_getmatrixcontent(df)
    elif __tf and (isinstance(x, __tf.Variable) or isinstance(x, __tf.Tensor)):
        df = __K.get_value(x)
        return _amphi_metadatapanel_getmatrixcontent(df)
    elif __torch and isinstance(x, __torch.Tensor):
        df = x.cpu().numpy()
        return _amphi_metadatapanel_getmatrixcontent(df)
    elif __xr and isinstance(x, __xr.DataArray):
        df = x.to_numpy()
        return _amphi_metadatapanel_getmatrixcontent(df)
    elif isinstance(x, list):
        s = __pd.Series(x)
        return _amphi_metadatapanel_getmatrixcontent(s)
  
  
def _amphi_metadatapanel_displaywidget(widget):
    display(widget)
  
  
def _amphi_metadatapanel_default(o):
    if isinstance(o, __np.number): return int(o)  
    raise TypeError
  
def _amphi_metadatapanel_deletevariable(x):
    exec("del %s" % x, globals())

def _amphi_metadatapanel_deleteallvariables():
    camel_case_pattern = re.compile(r'^[a-z]+(?:[A-Z][a-z]+)*(?:\\d+)?$')
    variable_names = []
    for key, value in list(globals().items()):
        if not key.startswith('_') and not hasattr(__builtins__, key) and not key in ['exit', 'quit', 'get_ipython', 'In', 'Out', 'Session', 'session', 'warehouse'] and not isinstance(value, (type(sys), types.ModuleType)) and camel_case_pattern.match(key):
            exec("del %s" % key, globals())

def __amphi_display_dataframe(df, dfName=None, nodeId=None, runtime=None):
    result_df = None  # Initialize result_df

    # Check if the input is a pandas DataFrame
    if __pd and isinstance(df, __pd.DataFrame):
        runtime = runtime or "local (pandas)"
        result_df = df.copy()
        result_df.columns = [f"{col} ({df[col].dtype})" for col in df.columns]

    elif mpd and isinstance(x, mpd.DataFrame):
        runtime = runtime or "Snowflake (Snowpark pandas API)"
        result_df = df.copy()
        result_df.columns = [f"{col} ({df[col].dtype})" for col in df.columns]

    # Check if the input is an Ibis Table
    elif "ibis" in globals() and isinstance(df, ibis.expr.types.Table):
        runtime = runtime or "ibis"
        schema = df.schema()
        result_df = df.execute()
        result_df.columns = [
            f"{col} ({dtype})" for col, dtype in schema.items()
        ]

    # If result_df is set, display with metadata
    if result_df is not None:
        metadata = {
            'runtime': runtime,
            'nodeId': nodeId if nodeId else None,
            'dfName': dfName if dfName else None
        }
        display(result_df, metadata=metadata)
    else:
        raise ValueError("Unsupported dataframe type: The provided dataframe is neither a pandas DataFrame nor an ibis Table.")


def __amphi_display_pandas_dataframe(df, dfName=None, nodeId=None, runtime="local (pandas)"):
    df_with_types = df.copy()
    df_with_types.columns = [f"{col} ({df[col].dtype})" for col in df.columns]

    # Use the parameters to define metadata
    metadata = {}
    metadata['runtime'] = runtime
    if nodeId:
        metadata['nodeId'] = nodeId
    if dfName:
        metadata['dfName'] = dfName

    display(df_with_types, metadata=metadata)

def _amphi_display_documents_as_html(documents):
    html_content = "<div id='documents'>"
    total_docs = len(documents)
    maxDoc = 10
    
    if total_docs > maxDoc:
        # Display first maxDoc // 2 documents
        for i, doc in enumerate(documents[:(maxDoc // 2)]):
            html_content += "<div class='_amphi_document'>"
            html_content += f"<div class='_amphi_nb'>{i+1}</div>"
            html_content += f"<div class='_amphi_page_content'><strong>Document Content:</strong> {doc.page_content}</div>"
            html_content += f"<div class='_amphi_metadata'><strong>Metadata:</strong> {doc.metadata}</div>"
            html_content += "</div>"
        
        # Ellipsis to indicate skipped documents
        html_content += "<div>...</div>"
        
        # Display last maxDoc // 2 documents
        for i, doc in enumerate(documents[-(maxDoc // 2):], start=total_docs - (maxDoc // 2)):
            html_content += "<div class='_amphi_document'>"
            html_content += f"<div class='_amphi_nb'>{i+1}</div>"
            html_content += f"<div class='_amphi_page_content'><strong>Document Content:</strong> {doc.page_content}</div>"
            html_content += f"<div class='_amphi_metadata'><strong>Metadata:</strong> {doc.metadata}</div>"
            html_content += "</div>"
    else:
        # Display all documents if total is maxDoc or less
        for i, doc in enumerate(documents):
            html_content += "<div class='_amphi_document'>"
            html_content += f"<div class='_amphi_nb'>{i+1}</div>"
            html_content += f"<div class='_amphi_page_content'><strong>Document Content:</strong> {doc.page_content}</div>"
            html_content += f"<div class='_amphi_metadata'><strong>Metadata:</strong> {doc.metadata}</div>"
            html_content += "</div>"
    
    html_content += "</div>"
    display(HTML(html_content))
`;
Languages.scripts = {
    python3: {
        initScript: Languages.py_script,
        queryCommand: '_amphi_metadatapanel_dict_list()',
        matrixQueryCommand: '_amphi_metadatapanel_getmatrixcontent',
        widgetQueryCommand: '_amphi_metadatapanel_displaywidget',
        deleteCommand: '_amphi_metadatapanel_deletevariable',
        deleteAllCommand: '_amphi_metadatapanel_deleteallvariables'
    },
    python2: {
        initScript: Languages.py_script,
        queryCommand: '_amphi_metadatapanel_dict_list()',
        matrixQueryCommand: '_amphi_metadatapanel_getmatrixcontent',
        widgetQueryCommand: '_amphi_metadatapanel_displaywidget',
        deleteCommand: '_amphi_metadatapanel_deletevariable',
        deleteAllCommand: '_amphi_metadatapanel_deleteallvariables'
    },
    python: {
        initScript: Languages.py_script,
        queryCommand: '_amphi_metadatapanel_dict_list()',
        matrixQueryCommand: '_amphi_metadatapanel_getmatrixcontent',
        widgetQueryCommand: '_amphi_metadatapanel_displaywidget',
        deleteCommand: '_amphi_metadatapanel_deletevariable',
        deleteAllCommand: '_amphi_metadatapanel_deleteallvariables'
    }
};



/***/ }),

/***/ "./lib/kernelconnector.js":
/*!********************************!*\
  !*** ./lib/kernelconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KernelConnector: () => (/* binding */ KernelConnector)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Connector class that handles execute request to a kernel
 */
class KernelConnector {
    constructor(options) {
        this._kernelRestarted = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._session = options.session;
        this._session.statusChanged.connect((sender, newStatus) => {
            switch (newStatus) {
                case 'restarting':
                    this._kernelRestarted.emit(this._session.ready);
                    break;
                case 'autorestarting':
                    this._kernelRestarted.emit(this._session.ready);
                    break;
                default:
                    break;
            }
        });
    }
    get kernelRestarted() {
        return this._kernelRestarted;
    }
    get kernelLanguage() {
        var _a;
        if (!((_a = this._session.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
            return Promise.resolve('');
        }
        return this._session.session.kernel.info.then(infoReply => {
            return infoReply.language_info.name;
        });
    }
    get kernelName() {
        return this._session.kernelDisplayName;
    }
    /**
     *  A Promise that is fulfilled when the session associated w/ the connector is ready.
     */
    get ready() {
        return this._session.ready;
    }
    /**
     *  A signal emitted for iopub messages of the kernel associated with the kernel.
     */
    get iopubMessage() {
        return this._session.iopubMessage;
    }
    /**
     * Executes the given request on the kernel associated with the connector.
     * @param content: IExecuteRequestMsg to forward to the kernel.
     * @param ioCallback: Callable to forward IOPub messages of the kernel to.
     * @returns Promise<KernelMessage.IExecuteReplyMsg>
     */
    fetch(content, ioCallback) {
        var _a;
        const kernel = (_a = this._session.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Require kernel to perform variable inspection!'));
        }
        const future = kernel.requestExecute(content);
        future.onIOPub = (msg) => {
            ioCallback(msg);
        };
        return future.done;
    }
    execute(content) {
        var _a;
        if (!((_a = this._session.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
            throw new Error('No session available.');
        }
        return this._session.session.kernel.requestExecute(content);
    }
}


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MetadataPanelManager: () => (/* binding */ MetadataPanelManager)
/* harmony export */ });
/**
 * A class that manages variable inspector widget instances and offers persistent
 * `IMetadataPanel` instance that other plugins can communicate with.
 */
class MetadataPanelManager {
    constructor() {
        this._source = null;
        this._panel = null;
        this._handlers = {};
    }
    hasHandler(id) {
        if (this._handlers[id]) {
            return true;
        }
        else {
            return false;
        }
    }
    getHandler(id) {
        return this._handlers[id];
    }
    addHandler(handler) {
        this._handlers[handler.id] = handler;
    }
    /**
     * The current inspector panel.
     */
    get panel() {
        return this._panel;
    }
    set panel(panel) {
        if (this.panel === panel) {
            return;
        }
        this._panel = panel;
        if (panel && !panel.source) {
            panel.source = this._source;
        }
    }
    /**
     * The source of events the inspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // remove subscriptions
        if (this._source) {
            this._source.disposed.disconnect(this._onSourceDisposed, this);
        }
        this._source = source;
        if (this._panel && !this._panel.isDisposed) {
            this._panel.source = this._source;
        }
        // Subscribe to new source
        if (this._source) {
            this._source.disposed.connect(this._onSourceDisposed, this);
        }
    }
    _onSourceDisposed() {
        this._source = null;
    }
}


/***/ }),

/***/ "./lib/metadatapanel.js":
/*!******************************!*\
  !*** ./lib/metadatapanel.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MetadataPanelPanel: () => (/* binding */ MetadataPanelPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);



const TITLE_CLASS = 'amphi-MetadataPanel-title';
const PANEL_CLASS = 'amphi-MetadataPanel';
const TABLE_CLASS = 'amphi-MetadataPanel-table';
const TABLE_BODY_CLASS = 'amphi-MetadataPanel-content';
const TABLE_ROW_CLASS = 'amphi-MetadataPanel-table-row';
const TABLE_NAME_CLASS = 'amphi-MetadataPanel-varName';
/**
 * A panel that renders the variables
 */
class MetadataPanelPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor(app) {
        super();
        this._source = null;
        this.app = app;
        this.addClass(PANEL_CLASS);
        this._title = Private.createTitle();
        this._title.className = TITLE_CLASS;
        this._table = Private.createTable();
        this._table.className = TABLE_CLASS;
        this.node.appendChild(this._title);
        this.node.appendChild(this._table);
    }
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            // this._source.performInspection();
            return;
        }
        //Remove old subscriptions
        if (this._source) {
            this._source.inspected.disconnect(this.onInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        this._source = source;
        //Subscribe to new object
        if (this._source) {
            this._source.inspected.connect(this.onInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
            this._source.performInspection();
        }
    }
    /**
     * Dispose resources
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    onInspectorUpdate(sender, allArgs) {
        console.log("Update detected");
        if (!this.isAttached) {
            return;
        }
        const title = allArgs.title;
        const args = allArgs.payload;
        //Render new variable state
        let row;
        this._table.deleteTFoot();
        this._table.createTFoot();
        this._table.tFoot.className = TABLE_BODY_CLASS;
        let lastNameToPreview = '';
        for (let index = 0; index < args.length; index++) {
            const item = args[index];
            const name = item.varName;
            const varType = item.varType;
            row = this._table.tFoot.insertRow();
            row.className = TABLE_ROW_CLASS;
            // Add onclick event for PREVIEW
            let previewCell = row.insertCell(0);
            if (item.isMatrix) {
                previewCell.title = 'View Preview';
                previewCell.className = 'amphi-MetadataPanel-previewButton';
                const previewIcon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.searchIcon.element();
                previewIcon.onclick = (ev) => {
                    var _a;
                    const command = 'pipeline-console:open';
                    this.app.commands.execute(command, {}).catch(reason => {
                        console.error(`An error occurred during the execution of ${command}.\n${reason}`);
                    });
                    (_a = this._source) === null || _a === void 0 ? void 0 : _a.performPreview(name).then((htmlData) => {
                        // this._showSample(htmlData, name);
                        // Open new widget rendering htmlData
                    });
                };
                previewCell.append(previewIcon);
            }
            else {
                previewCell.innerHTML = ''; // Or handle non-matrix items differently
            }
            // Correctly assign name to a new cell
            let nameCell = row.insertCell(1);
            nameCell.className = TABLE_NAME_CLASS; // Ensure this is the correct class name
            nameCell.innerHTML = '<b>' + name + '</b><br><small><i>' + item.varShape + '</i></small>';
            let contentCell = row.insertCell(2);
            contentCell.innerHTML = item.varContent.split(',').join('<br>');
            lastNameToPreview = name;
        }
        const tFoot = this._table.tFoot;
        if (tFoot) {
            const rows = Array.from(tFoot.rows);
            for (let i = rows.length - 1; i >= 0; i--) {
                tFoot.appendChild(rows[i]); // Re-append each row in reverse order
            }
            // this._source.performPreview(lastNameToPreview) // Add a name
        }
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    _showSample(htmlData, name) {
        // Create a custom widget to display the HTML content
        const sample = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        sample.node.innerHTML = htmlData; // Inject HTML data directly into the widget's node
        sample.node.className = "preview_data";
        sample.title.label = name;
        sample.title.closable = true;
        sample.id = 'widget-' + new Date().getTime() + '-' + Math.random().toString(36).substr(2, 9);
        const metadataPanelId = 'amphi-logConsole'; // Using the provided log console panel ID
        let variableInspectorPanel = null;
        // Iterate over each widget in the 'main' area to find the log console
        for (const widget of this.app.shell.widgets('main')) {
            if (widget.id === metadataPanelId) {
                variableInspectorPanel = widget;
                break;
            }
        }
        this.app.shell.add(sample, 'main', { ref: variableInspectorPanel.id, mode: 'tab-after' });
        this.app.shell.activateById(sample.id);
    }
    _showMatrix(dataModel, name, varType) {
        const datagrid = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.DataGrid();
        datagrid.dataModel = dataModel;
        datagrid.title.label = varType + ': ' + name;
        datagrid.title.closable = true;
        const lout = this.parent.layout;
        lout.addWidget(datagrid);
        // lout.addWidget(datagrid, { mode: 'split-right' });
        //todo activate/focus matrix widget
    }
}
var Private;
(function (Private) {
    const entityMap = new Map(Object.entries({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;'
    }));
    function escapeHtml(source) {
        return String(source).replace(/[&<>"'/]/g, (s) => entityMap.get(s));
    }
    Private.escapeHtml = escapeHtml;
    function createTable() {
        const table = document.createElement('table');
        table.createTHead();
        const hrow = table.tHead.insertRow(0);
        const cell2 = hrow.insertCell(0);
        cell2.innerHTML = '';
        const cell3 = hrow.insertCell(1);
        cell3.innerHTML = 'Component Output';
        /*
        const cell4 = hrow.insertCell(2);
        cell4.innerHTML = 'Rows';
        */
        const cell5 = hrow.insertCell(2);
        cell5.innerHTML = 'Schema';
        return table;
    }
    Private.createTable = createTable;
    function createTitle(header = '') {
        const title = document.createElement('p');
        title.innerHTML = header;
        return title;
    }
    Private.createTitle = createTitle;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IMetadataPanel: () => (/* binding */ IMetadataPanel),
/* harmony export */   IMetadataPanelManager: () => (/* binding */ IMetadataPanelManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IMetadataPanelManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab_extension/metadatapanel:IMetadataPanelManager');
/**
 * The inspector panel token.
 */
const IMetadataPanel = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab_extension/metadatapanel:IMetadataPanel');


/***/ })

}]);
//# sourceMappingURL=lib_index_js.28ea3f2cd08895eb74a9.js.map