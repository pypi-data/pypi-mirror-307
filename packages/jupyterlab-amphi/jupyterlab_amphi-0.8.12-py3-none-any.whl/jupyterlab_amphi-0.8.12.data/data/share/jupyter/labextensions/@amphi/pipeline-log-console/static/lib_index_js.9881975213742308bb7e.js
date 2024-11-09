"use strict";
(self["webpackChunk_amphi_pipeline_log_console"] = self["webpackChunk_amphi_pipeline_log_console"] || []).push([["lib_index_js"],{

/***/ "./lib/DataView.js":
/*!*************************!*\
  !*** ./lib/DataView.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/tag/index.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/table/index.js");


const DataView = ({ htmlData }) => {
    const [dataSource, setDataSource] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [columns, setColumns] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const { data, headers } = htmlToJson(htmlData);
        setDataSource(data);
        setColumns(headers.map((header, index) => {
            // Extract the type in parentheses at the end of the header
            const matches = header.match(/^(.*)\s\(([^)]+)\)$/); // Match pattern "ColumnName (type)"
            const columnName = matches ? matches[1] : header;
            const columnType = matches ? matches[2] : null;
            return {
                title: index === 0 ? '' : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { whiteSpace: 'nowrap' } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, columnName),
                        columnType && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__["default"], { style: { fontSize: '10px', marginTop: '4px', color: '#5F9A97' } }, columnType))))),
                dataIndex: header,
                key: header,
                ...(index === 0 && { rowScope: 'row' }),
                ellipsis: true,
                render: (text) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                        fontSize: '12px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        maxWidth: '200px',
                        minWidth: '25px'
                    } }, text)),
            };
        }));
    }, [htmlData]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__["default"], { dataSource: dataSource, columns: columns, pagination: false, size: "small", scroll: { x: 'max-content' }, style: { fontSize: '12px', tableLayout: 'fixed', minWidth: '100%' } }));
};
function htmlToJson(htmlString) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    // Extract headers from th inside thead, excluding the first one (index)
    let headers = Array.from(doc.querySelectorAll('table thead th')).slice(1).map(th => { var _a, _b; return (_b = (_a = th.textContent) === null || _a === void 0 ? void 0 : _a.trim()) !== null && _b !== void 0 ? _b : ""; });
    const rows = doc.querySelectorAll('table tbody tr');
    const data = Array.from(rows, row => {
        var _a, _b;
        const cells = row.querySelectorAll('th, td');
        const rowObj = {};
        // Capture the index from the first cell
        rowObj['index'] = (_b = (_a = cells[0].textContent) === null || _a === void 0 ? void 0 : _a.trim()) !== null && _b !== void 0 ? _b : "";
        // Map the rest of the cells to headers
        headers.forEach((header, idx) => {
            var _a, _b, _c;
            rowObj[header] = (_c = (_b = (_a = cells[idx + 1]) === null || _a === void 0 ? void 0 : _a.textContent) === null || _b === void 0 ? void 0 : _b.trim()) !== null && _c !== void 0 ? _c : "";
        });
        return rowObj;
    });
    return { data, headers: ['index', ...headers] }; // Set the first header to empty string
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DataView);


/***/ }),

/***/ "./lib/DocumentView.js":
/*!*****************************!*\
  !*** ./lib/DocumentView.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/tree/index.js");


const parseHTMLToJSON = (htmlContent) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    const documentElements = doc.querySelectorAll('#documents > div._amphi_document');
    const documents = [];
    documentElements.forEach((element) => {
        var _a, _b, _c;
        const nbElement = element.querySelector('div._amphi_nb');
        const pageContentElement = element.querySelector('div._amphi_page_content');
        const metadataElement = element.querySelector('div._amphi_metadata');
        if (nbElement && pageContentElement && metadataElement) {
            const nb = ((_a = nbElement.textContent) === null || _a === void 0 ? void 0 : _a.trim()) || '';
            const pageContent = ((_b = pageContentElement.innerHTML) === null || _b === void 0 ? void 0 : _b.replace('<strong>Document Content:</strong>', '').trim()) || '';
            let metadataText = ((_c = metadataElement.textContent) === null || _c === void 0 ? void 0 : _c.replace('Metadata:', '').trim()) || '';
            let metadata;
            try {
                metadataText = metadataText.replace(/'/g, '"'); // Replace single quotes with double quotes
                metadata = JSON.parse(metadataText);
            }
            catch (e) {
                console.error("Error parsing metadata:", e);
                metadata = metadataText; // Fall back to raw text if parsing fails
            }
            documents.push({ nb, page_content: pageContent, metadata: metadata });
        }
    });
    return documents;
};
const createTreeData = (documents) => {
    return documents.map((doc, index) => ({
        title: doc.nb,
        key: `doc-${index}`,
        children: [
            {
                title: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("pre", { style: { userSelect: 'text', cursor: 'text' } }, doc.page_content)),
                key: `doc-${index}-page-content`
            },
            {
                title: 'Metadata',
                key: `doc-${index}-metadata`,
                children: Object.entries(doc.metadata).map(([key, value]) => ({
                    title: `${key}: ${value}`,
                    key: `doc-${index}-metadata-${key}`
                }))
            }
        ]
    }));
};
const DocumentView = ({ htmlData }) => {
    const documents = parseHTMLToJSON(htmlData);
    const treeData = createTreeData(documents);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__["default"], { defaultExpandedKeys: treeData.map(node => node.key), defaultSelectedKeys: treeData.map(node => node.key), defaultCheckedKeys: treeData.map(node => node.key), treeData: treeData }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DocumentView);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PipelineConsoleHandler: () => (/* binding */ PipelineConsoleHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

class AbstractHandler {
    constructor(connector) {
        this._isDisposed = false;
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._rendermime = null;
        this._connector = connector;
    }
    get disposed() {
        return this._disposed;
    }
    get isDisposed() {
        return this._isDisposed;
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
}
/**
 * An object that handles code inspection.
 */
class PipelineConsoleHandler extends AbstractHandler {
    constructor(options) {
        var _a;
        super(options.connector);
        this._id = options.id;
        this._rendermime = (_a = options.rendermime) !== null && _a !== void 0 ? _a : null;
        this._ready = this._connector.ready;
        this._connector.kernelRestarted.connect((sender, kernelReady) => {
            const title = {
                contextName: '<b>Restarting kernel...</b> '
            };
            this._ready = this._connector.ready;
        });
    }
    get id() {
        return this._id;
    }
    get ready() {
        return this._ready;
    }
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   clockIcon: () => (/* binding */ clockIcon),
/* harmony export */   cpuIcon: () => (/* binding */ cpuIcon),
/* harmony export */   gridIcon: () => (/* binding */ gridIcon),
/* harmony export */   pipelineIcon: () => (/* binding */ pipelineIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_clock_16_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/clock-16.svg */ "./style/icons/clock-16.svg");
/* harmony import */ var _style_icons_grid_16_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/grid-16.svg */ "./style/icons/grid-16.svg");
/* harmony import */ var _style_icons_cpu_16_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/cpu-16.svg */ "./style/icons/cpu-16.svg");
/* harmony import */ var _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/pipeline-16.svg */ "./style/icons/pipeline-16.svg");





const clockIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:clock-icon',
    svgstr: _style_icons_clock_16_svg__WEBPACK_IMPORTED_MODULE_1__
});
const pipelineIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipeline-console-icon',
    svgstr: _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_2__
});
const gridIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:grid-console-icon',
    svgstr: _style_icons_grid_16_svg__WEBPACK_IMPORTED_MODULE_3__
});
const cpuIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:cpu-icon',
    svgstr: _style_icons_cpu_16_svg__WEBPACK_IMPORTED_MODULE_4__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @amphi/pipeline-editor */ "webpack/sharing/consume/default/@amphi/pipeline-editor");
/* harmony import */ var _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./kernelconnector */ "./lib/kernelconnector.js");
/* harmony import */ var _logconsole__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./logconsole */ "./lib/logconsole.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");












var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'pipeline-console:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing variable introspection.
 */
const logsconsole = {
    id: '@amphi/pipeline-log-console:extension',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_5__.IPipelineTracker],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_6__.IPipelineConsoleManager,
    autoStart: true,
    activate: (app, palette, restorer, labShell, settings, pipelines) => {
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_7__.LogConsoleManager();
        const category = 'Pipeline Console';
        const command = CommandIDs.open;
        const label = 'Pipeline Console';
        const namespace = 'pipeline-console';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({ namespace });
        let maxPreview = 80;
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            maxPreview = setting.get('maxPreview').composite;
            console.log(`Settings Example extension: maxPreview is set to '${maxPreview}'`);
        }
        Promise.all([app.restored, settings.load('@amphi/pipeline-log-console:extension')])
            .then(([, setting]) => {
            // Read the settings
            loadSetting(setting);
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            /**
             * Create and track a new inspector.
             */
            function newPanel() {
                // Get the current widget from the lab shell
                const currentWidget = labShell.currentWidget;
                // Ensure the current widget is a pipeline and has a context
                if (!currentWidget || !pipelines.has(currentWidget)) {
                    console.warn('No active pipeline to provide context.');
                    return;
                }
                const pipelinePanel = currentWidget;
                const context = pipelinePanel.context;
                const panel = new _logconsole__WEBPACK_IMPORTED_MODULE_8__.PipelineConsolePanel(app, app.commands, context);
                panel.id = 'amphi-logConsole';
                panel.title.label = 'Pipeline Console';
                panel.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.listIcon;
                panel.title.closable = true;
                panel.disposed.connect(() => {
                    if (manager.panel === panel) {
                        manager.panel = null;
                    }
                });
                // Track the inspector panel
                tracker.add(panel);
                return panel;
            }
            // Add command to palette
            app.commands.addCommand(command, {
                label,
                execute: () => {
                    const metadataPanelId = 'amphi-metadataPanel'; // Using the provided log console panel ID
                    let metadataPanel = null;
                    // Iterate over each widget in the 'main' area to find the log console
                    for (const widget of app.shell.widgets('main')) {
                        if (widget.id === metadataPanelId) {
                            metadataPanel = widget;
                            break;
                        }
                    }
                    if (!manager.panel || manager.panel.isDisposed) {
                        manager.panel = newPanel();
                    }
                    // Check if the metadata panel is found and is attached
                    if (metadataPanel && metadataPanel.isAttached) {
                        // If log console panel is open, add the preview panel as a tab next to it
                        if (!manager.panel.isAttached) {
                            app.shell.add(manager.panel, 'main', { ref: metadataPanel.id, mode: 'tab-after' });
                        }
                    }
                    else {
                        // If log console panel is not open, open the preview panel in split-bottom mode
                        if (!manager.panel.isAttached) {
                            app.shell.add(manager.panel, 'main', { mode: 'split-bottom' });
                        }
                    }
                    app.shell.activateById(manager.panel.id);
                }
            });
            palette.addItem({ command, category });
            app.commands.addCommand('pipeline-console:clear', {
                execute: () => {
                    manager.panel.clearLogs();
                },
                label: 'Clear Console'
            });
            app.commands.addCommand('pipeline-console:settings', {
                execute: () => {
                },
                label: 'Console Settings'
            });
            app.contextMenu.addItem({
                command: 'pipeline-console:clear',
                selector: '.amphi-Console',
                rank: 1
            });
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
        // Enable state restoration
        restorer.restore(tracker, {
            command,
            args: () => ({}),
            name: () => 'amphi-logConsole'
        });
        console.log('JupyterLab extension @amphi/pipeline-log-console is activated!');
        return manager;
    }
};
/**
 * An extension that registers pipelines for variable inspection.
 */
const pipelines = {
    id: '@amphi/pipeline-log-console:pipelines',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_6__.IPipelineConsoleManager, _amphi_pipeline_editor__WEBPACK_IMPORTED_MODULE_5__.IPipelineTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    autoStart: true,
    activate: (app, manager, pipelines, labShell) => {
        const handlers = {};
        function formatLogDate(date) {
            const dateObj = new Date(date);
            return `${dateObj.toLocaleDateString()}\n${dateObj.toLocaleTimeString()}`;
        }
        /**
         * Subscribes to the creation of new pipelines. If a new pipeline is created, build a new handler for the pipelines.
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
                    const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_9__.KernelConnector({ session });
                    const options = {
                        connector: connector,
                        id: session.path //Using the sessions path as an identifier for now.
                    };
                    const handler = new _handler__WEBPACK_IMPORTED_MODULE_10__.PipelineConsoleHandler(options);
                    manager.addHandler(handler);
                    pipelinePanel.disposed.connect(() => {
                        delete handlers[pipelinePanel.id];
                        handler.dispose();
                    });
                    handler.ready.then(() => {
                        resolve(handler);
                        connector.ready.then(async () => {
                            session.session.kernel.anyMessage.connect((sender, args) => {
                                if (manager.panel) {
                                    if (args.direction === 'recv') {
                                        // Filter and process kernel messages here
                                        // For example, args.msg.header.msg_type might be 'stream' for log messages
                                        if (args.msg.header.msg_type === 'execute_result' || args.msg.header.msg_type === 'display_data') {
                                            // Assert the message type to IExecuteResultMsg or IDisplayDataMsg to access 'data'
                                            const content = args.msg.content;
                                            if (content.data['text/html']) {
                                                manager.panel.onNewLog(formatLogDate(args.msg.header.date), session.name, "data", content.data['text/html'], content.metadata);
                                            }
                                        }
                                        else if (args.msg.header.msg_type === 'stream') {
                                            const streamMsg = args.msg;
                                            if (streamMsg.content.text && streamMsg.content.text !== '\n') {
                                                // Create a container div for the content
                                                const streamText = document.createElement('div');
                                                console.log("streamMsg.content.text %o", streamMsg.content.text);
                                                // Directly set innerHTML with replaced newlines, avoiding renderText to prevent duplication
                                                streamText.innerHTML = streamMsg.content.text.replace(/\n/g, '<br>');
                                                // Convert the entire structure to HTML string if necessary
                                                const streamHTML = streamText.outerHTML;
                                                manager.panel.onNewLog(formatLogDate(args.msg.header.date), session.name, "info", streamHTML, null);
                                            }
                                        }
                                        else if (args.msg.header.msg_type === 'error') {
                                            // Handle error messages
                                            const errorMsg = args.msg; // If using TypeScript
                                            const traceback = errorMsg.content.traceback.join('\n');
                                            const errorId = `traceback-${Date.now()}`; // Unique ID for the traceback container
                                            // Create a container for the error message and the link
                                            const errorContainer = document.createElement('div');
                                            const errorMessageText = `${errorMsg.content.evalue}`;
                                            // Ensure the link has a unique ID that matches the pattern for event delegation
                                            // Can do better here, ... TODO
                                            errorContainer.innerHTML = `<pre><span>${errorMessageText}</span><br><a href="#" style="text-decoration: underline; color: grey;" id="link-${errorId}" onClick="document.getElementById('${errorId}').style.display = document.getElementById('${errorId}').style.display === 'none' ? 'block' : 'none'; return false;">Show Traceback</a></pre>`;
                                            // Create a container for the traceback, initially hidden
                                            const tracebackContainer = document.createElement('pre');
                                            tracebackContainer.id = errorId;
                                            tracebackContainer.style.display = 'none';
                                            errorContainer.appendChild(tracebackContainer);
                                            // Use the sanitizer to safely render the traceback
                                            const options = {
                                                host: tracebackContainer,
                                                source: traceback,
                                                sanitizer: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Sanitizer(), // Use the default sanitizer
                                            };
                                            (0,_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.renderText)(options).then(() => {
                                                // Once the traceback is sanitized and rendered, append it to the errorContainer
                                                // Convert the entire structure to HTML string if necessary
                                                const errorHTML = errorContainer.outerHTML;
                                                manager.panel.onNewLog(formatLogDate(errorMsg.header.date), session.name, "error", errorHTML, null);
                                            });
                                        }
                                    }
                                }
                            });
                        });
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
                    // manager.source.performInspection();
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
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    logsconsole,
    pipelines
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


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
    execute(content) {
        var _a;
        if (!((_a = this._session.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
            throw new Error('No session available.');
        }
        return this._session.session.kernel.requestExecute(content);
    }
}


/***/ }),

/***/ "./lib/logconsole.js":
/*!***************************!*\
  !*** ./lib/logconsole.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PipelineConsolePanel: () => (/* binding */ PipelineConsolePanel)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _DataView__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./DataView */ "./lib/DataView.js");
/* harmony import */ var _DocumentView__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./DocumentView */ "./lib/DocumentView.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/tag/index.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/alert/index.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! antd */ "../../node_modules/antd/es/divider/index.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");







const TITLE_CLASS = 'amphi-Console-title';
const PANEL_CLASS = 'amphi-Console';
const TABLE_CLASS = 'amphi-Console-table';
const TABLE_BODY_CLASS = 'amphi-Console-content';
const TABLE_ROW_CLASS = 'amphi-Console-table-row';
const SINGLE_COLUMN_CLASS = 'amphi-Console-single-column'; // New class for single column
/**
 * A panel that renders the pipeline logs
 */
class PipelineConsolePanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(app, commands, context) {
        super();
        this._source = null;
        this._app = app; // Assign the app object
        this._commands = commands;
        this._context = context;
        this.addClass(PANEL_CLASS);
        this._title = Private.createTitle();
        this._title.className = TITLE_CLASS;
        this._console = Private.createConsole();
        this._console.className = TABLE_CLASS;
        this.node.appendChild(this._title);
        this.node.appendChild(this._console);
    }
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // Remove old subscriptions
        if (this._source) {
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        this._source = source;
        // Subscribe to new object
        if (this._source) {
            this._source.disposed.connect(this.onSourceDisposed, this);
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
    onNewLog(date, pipelineName, level, content, metadata) {
        if (!this.isAttached) {
            return;
        }
        // Ensure the table footer exists
        if (!this._console.tFoot) {
            this._console.createTFoot();
            this._console.tFoot.className = TABLE_BODY_CLASS;
        }
        // Insert a new row at the beginning of the table footer
        let row = this._console.tFoot.insertRow(0);
        row.className = `${TABLE_ROW_CLASS} ${SINGLE_COLUMN_CLASS}`; // Add single column class
        // Add a single cell to the new row
        let singleCell = row.insertCell(0);
        singleCell.style.padding = "5px";
        singleCell.className = SINGLE_COLUMN_CLASS;
        let dateTag;
        let pipelineNameTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.pipelineIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, pipelineName);
        let dataframeSizeTag = null;
        let nodeIdTag = null;
        let runtimeTag = null;
        let contentComponent;
        let viewData = null;
        switch (level) {
            case "info":
                dateTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.clockIcon.react, { className: "anticon" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, date);
                contentComponent = (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_5__["default"], { showIcon: true, banner: true, message: react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { dangerouslySetInnerHTML: { __html: content } }), type: /SUCCESS/i.test(content) ? "success" : /ERROR|WARNING/i.test(content) ? "warning" : "info" }));
                break;
            case "error":
                dateTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.clockIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, date);
                contentComponent = (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_5__["default"], { message: "Error", banner: true, showIcon: true, description: react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { dangerouslySetInnerHTML: { __html: content.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;') } }), type: "error" }));
                break;
            case "data":
                dateTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.clockIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, date);
                nodeIdTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.clockIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, metadata.nodeId);
                runtimeTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.cpuIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, metadata.runtime);
                viewData = (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, onClick: () => this._commands.execute('pipeline-editor-component:view-data', { nodeId: metadata.nodeId, context: this._context }), icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.clockIcon.react, { className: "anticon amphi-Console-icon-size" }), color: "#44776D", style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, "View data"));
                const parser = new DOMParser();
                const doc = parser.parseFromString(content, 'text/html');
                const firstDiv = doc.querySelector('div');
                if (firstDiv && firstDiv.id === 'documents') {
                    contentComponent = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_DocumentView__WEBPACK_IMPORTED_MODULE_6__["default"], { htmlData: content });
                }
                else {
                    // Extract dataframe size from the last paragraph if it exists
                    const sizeElement = doc.querySelector('p:last-of-type');
                    let dataframeSize = null;
                    if (sizeElement && sizeElement.textContent.includes('rows ×')) {
                        dataframeSize = sizeElement.textContent.trim();
                    }
                    if (dataframeSize) {
                        dataframeSizeTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false, icon: react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.gridIcon.react, { className: "anticon amphi-Console-icon-size" }), style: { whiteSpace: 'normal', wordWrap: 'break-word' } }, dataframeSize);
                    }
                    contentComponent = (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_DataView__WEBPACK_IMPORTED_MODULE_7__["default"], { htmlData: content })));
                }
                break;
            default:
                dateTag = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_3__["default"], { bordered: false }, date);
                contentComponent = react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, content);
        }
        // Render tags and content inside the single cell
        react_dom__WEBPACK_IMPORTED_MODULE_2___default().render(react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { display: 'flex', flexDirection: 'column', gap: '4px' } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0px', marginBottom: '2px' } },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { display: 'flex', alignItems: 'center', gap: '4px' } },
                    dateTag,
                    pipelineNameTag,
                    dataframeSizeTag,
                    runtimeTag),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null)),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, contentComponent),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(antd__WEBPACK_IMPORTED_MODULE_8__["default"], { style: { margin: '6px 0' } })), singleCell);
        // Scroll to the top
        this._console.parentElement.scrollTop = 0;
    }
    clearLogs() {
        // Check if table footer exists and remove all its rows
        if (this._console.tFoot) {
            while (this._console.tFoot.rows.length > 0) {
                this._console.tFoot.deleteRow(0);
            }
        }
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
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
    function createConsole() {
        const table = document.createElement('table');
        return table;
    }
    Private.createConsole = createConsole;
    function createTitle(header = '') {
        const title = document.createElement('p');
        title.innerHTML = header;
        return title;
    }
    Private.createTitle = createTitle;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LogConsoleManager: () => (/* binding */ LogConsoleManager)
/* harmony export */ });
/**
 * A class that manages variable inspector widget instances and offers persistent
 * `IMetadataPanel` instance that other plugins can communicate with.
 */
class LogConsoleManager {
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
     * The current console panel.
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

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IPipelineConsole: () => (/* binding */ IPipelineConsole),
/* harmony export */   IPipelineConsoleManager: () => (/* binding */ IPipelineConsoleManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IPipelineConsoleManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab_extension/logconsole:IPipelineConsoleManager');
/**
 * The inspector panel token.
 */
const IPipelineConsole = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab_extension/logconsole:IPipelineConsole');


/***/ }),

/***/ "./style/icons/clock-16.svg":
/*!**********************************!*\
  !*** ./style/icons/clock-16.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M8.5 3.75a.75.75 0 00-1.5 0V8c0 .284.16.544.415.67l2.5 1.25a.75.75 0 10.67-1.34L8.5 7.535V3.75z\"/><path fill-rule=\"evenodd\" d=\"M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/cpu-16.svg":
/*!********************************!*\
  !*** ./style/icons/cpu-16.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M6.25 5C5.56 5 5 5.56 5 6.25v3.5c0 .69.56 1.25 1.25 1.25h3.5c.69 0 1.25-.56 1.25-1.25v-3.5C11 5.56 10.44 5 9.75 5h-3.5zm.25 4.5v-3h3v3h-3z\"/><path d=\"M6.25.05a.7.7 0 01.7.7V2h2.1V.75a.7.7 0 111.4 0V2h1.3A2.25 2.25 0 0114 4.25v1.3h1.25a.7.7 0 110 1.4H14v2.1h1.25a.7.7 0 110 1.4H14v1.3A2.25 2.25 0 0111.75 14h-1.3v1.25a.7.7 0 11-1.4 0V14h-2.1v1.25a.7.7 0 11-1.4 0V14h-1.3A2.25 2.25 0 012 11.75v-1.3H.75a.7.7 0 110-1.4H2v-2.1H.75a.7.7 0 110-1.4H2v-1.3A2.25 2.25 0 014.25 2h1.3V.75a.7.7 0 01.7-.7zM3.5 4.25a.75.75 0 01.75-.75h7.5a.75.75 0 01.75.75v7.5a.75.75 0 01-.75.75h-7.5a.75.75 0 01-.75-.75v-7.5z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/grid-16.svg":
/*!*********************************!*\
  !*** ./style/icons/grid-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M2.25 1C1.56 1 1 1.56 1 2.25v3.5C1 6.44 1.56 7 2.25 7h3.5C6.44 7 7 6.44 7 5.75v-3.5C7 1.56 6.44 1 5.75 1h-3.5zm.25 4.5v-3h3v3h-3zM10.25 1C9.56 1 9 1.56 9 2.25v3.5C9 6.44 9.56 7 10.25 7h3.5C14.44 7 15 6.44 15 5.75v-3.5C15 1.56 14.44 1 13.75 1h-3.5zm.25 4.5v-3h3v3h-3zM9 10.25C9 9.56 9.56 9 10.25 9h3.5c.69 0 1.25.56 1.25 1.25v3.5c0 .69-.56 1.25-1.25 1.25h-3.5C9.56 15 9 14.44 9 13.75v-3.5zm1.5.25v3h3v-3h-3zM2.25 9C1.56 9 1 9.56 1 10.25v3.5c0 .69.56 1.25 1.25 1.25h3.5C6.44 15 7 14.44 7 13.75v-3.5C7 9.56 6.44 9 5.75 9h-3.5zm.25 4.5v-3h3v3h-3z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/pipeline-16.svg":
/*!*************************************!*\
  !*** ./style/icons/pipeline-16.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   width=\"16\"\n   height=\"16\"\n   fill=\"none\"\n   viewBox=\"0 0 16 16\"\n   version=\"1.1\"\n   id=\"svg1\"\n   sodipodi:docname=\"pipeline-16.svg\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs1\" />\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"14.75\"\n     inkscape:cx=\"8\"\n     inkscape:cy=\"8\"\n     inkscape:window-width=\"1312\"\n     inkscape:window-height=\"449\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"639\"\n     inkscape:window-maximized=\"0\"\n     inkscape:current-layer=\"svg1\" />\n  <path\n     fill=\"currentColor\"\n     fill-rule=\"evenodd\"\n     d=\"M2.75 2.5A1.75 1.75 0 001 4.25v1C1 6.216 1.784 7 2.75 7h1a1.75 1.75 0 001.732-1.5H6.5a.75.75 0 01.75.75v3.5A2.25 2.25 0 009.5 12h1.018c.121.848.85 1.5 1.732 1.5h1A1.75 1.75 0 0015 11.75v-1A1.75 1.75 0 0013.25 9h-1a1.75 1.75 0 00-1.732 1.5H9.5a.75.75 0 01-.75-.75v-3.5A2.25 2.25 0 006.5 4H5.482A1.75 1.75 0 003.75 2.5h-1zM2.5 4.25A.25.25 0 012.75 4h1a.25.25 0 01.25.25v1a.25.25 0 01-.25.25h-1a.25.25 0 01-.25-.25v-1zm9.75 6.25a.25.25 0 00-.25.25v1c0 .138.112.25.25.25h1a.25.25 0 00.25-.25v-1a.25.25 0 00-.25-.25h-1z\"\n     clip-rule=\"evenodd\"\n     id=\"path1\"\n     style=\"fill:#000000;fill-opacity:1\" />\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.9881975213742308bb7e.js.map