(self["webpackChunklibro_lab"] = self["webpackChunklibro_lab"] || []).push([[599],{

/***/ 49059:
/***/ (function(module) {

function webpackEmptyContext(req) {
	var e = new Error("Cannot find module '" + req + "'");
	e.code = 'MODULE_NOT_FOUND';
	throw e;
}
webpackEmptyContext.keys = function() { return []; };
webpackEmptyContext.resolve = webpackEmptyContext;
webpackEmptyContext.id = 49059;
module.exports = webpackEmptyContext;

/***/ }),

/***/ 28756:
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": function() { return /* binding */ dbgpt; }
});

// EXTERNAL MODULE: ./node_modules/@difizen/libro-lab/es/index.js + 400 modules
var es = __webpack_require__(46348);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/module/mana-module.js
var mana_module = __webpack_require__(17354);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-syringe/es/index.js + 15 modules
var mana_syringe_es = __webpack_require__(49383);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/components/index.js + 6 modules
var components = __webpack_require__(10533);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/index.js + 45 modules
var mana_app_es = __webpack_require__(77780);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/regeneratorRuntime.js
var regeneratorRuntime = __webpack_require__(15009);
var regeneratorRuntime_default = /*#__PURE__*/__webpack_require__.n(regeneratorRuntime);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/asyncToGenerator.js
var asyncToGenerator = __webpack_require__(99289);
var asyncToGenerator_default = /*#__PURE__*/__webpack_require__.n(asyncToGenerator);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/initializerDefineProperty.js
var initializerDefineProperty = __webpack_require__(19911);
var initializerDefineProperty_default = /*#__PURE__*/__webpack_require__.n(initializerDefineProperty);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/classCallCheck.js
var classCallCheck = __webpack_require__(12444);
var classCallCheck_default = /*#__PURE__*/__webpack_require__.n(classCallCheck);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createClass.js
var createClass = __webpack_require__(72004);
var createClass_default = /*#__PURE__*/__webpack_require__.n(createClass);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/applyDecoratedDescriptor.js
var applyDecoratedDescriptor = __webpack_require__(65371);
var applyDecoratedDescriptor_default = /*#__PURE__*/__webpack_require__.n(applyDecoratedDescriptor);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/initializerWarningHelper.js
var initializerWarningHelper = __webpack_require__(45966);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-jupyter/es/index.js + 430 modules
var libro_jupyter_es = __webpack_require__(52638);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/configuration/configuration-service.js
var configuration_service = __webpack_require__(52243);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/open-handler.js
var open_handler = __webpack_require__(70468);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-common/es/uri.js + 4 modules
var uri = __webpack_require__(26587);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/file-tree/file-tree-view.js + 2 modules
var file_tree_view = __webpack_require__(12084);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot-view-manager.js
var slot_view_manager = __webpack_require__(94104);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-terminal/es/index.js + 18 modules
var libro_terminal_es = __webpack_require__(93852);
// EXTERNAL MODULE: ./node_modules/query-string/index.js + 1 modules
var query_string = __webpack_require__(87449);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/application/application.js
var application = __webpack_require__(15910);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-manager.js
var view_manager = __webpack_require__(44659);
// EXTERNAL MODULE: ./node_modules/@difizen/magent-core/es/index.js + 57 modules
var magent_core_es = __webpack_require__(85526);
;// CONCATENATED MODULE: ./src/pages/dbgpt/app.ts







var _dec, _dec2, _dec3, _dec4, _dec5, _dec6, _dec7, _dec8, _dec9, _dec10, _dec11, _class, _class2, _descriptor, _descriptor2, _descriptor3, _descriptor4, _descriptor5, _descriptor6, _descriptor7, _descriptor8, _descriptor9, _descriptor10;









var ShouldPreventStoreViewKey = 'mana-should-prevent-store-view';
var LibroApp = (_dec = (0,mana_syringe_es/* singleton */.ri)({
  contrib: application/* ApplicationContribution */.rS
}), _dec2 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), _dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerManager */.ErZ), _dec4 = (0,mana_syringe_es/* inject */.f3)(view_manager/* ViewManager */.v), _dec5 = (0,mana_syringe_es/* inject */.f3)(slot_view_manager/* SlotViewManager */.I), _dec6 = (0,mana_syringe_es/* inject */.f3)(configuration_service/* ConfigurationService */.e), _dec7 = (0,mana_syringe_es/* inject */.f3)(es/* LayoutService */.Pb3), _dec8 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* FileCommandContribution */.uq5), _dec9 = (0,mana_syringe_es/* inject */.f3)(magent_core_es/* Fetcher */.HI), _dec10 = (0,mana_syringe_es/* inject */.f3)(open_handler/* OpenerService */.Bp), _dec11 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* LibroFileService */.tL0), _dec(_class = (_class2 = /*#__PURE__*/function () {
  function LibroApp() {
    classCallCheck_default()(this, LibroApp);
    initializerDefineProperty_default()(this, "serverConnection", _descriptor, this);
    initializerDefineProperty_default()(this, "serverManager", _descriptor2, this);
    initializerDefineProperty_default()(this, "viewManager", _descriptor3, this);
    initializerDefineProperty_default()(this, "slotViewManager", _descriptor4, this);
    initializerDefineProperty_default()(this, "configurationService", _descriptor5, this);
    initializerDefineProperty_default()(this, "layoutService", _descriptor6, this);
    initializerDefineProperty_default()(this, "fileCommandContribution", _descriptor7, this);
    initializerDefineProperty_default()(this, "fetcher", _descriptor8, this);
    initializerDefineProperty_default()(this, "openerService", _descriptor9, this);
    initializerDefineProperty_default()(this, "libroFileService", _descriptor10, this);
    this.location = void 0;
  }
  createClass_default()(LibroApp, [{
    key: "onStart",
    value: function () {
      var _onStart = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee2() {
        var _this = this;
        var baseUrl, el, pageConfig;
        return regeneratorRuntime_default()().wrap(function _callee2$(_context2) {
          while (1) switch (_context2.prev = _context2.next) {
            case 0:
              this.configurationService.set(libro_jupyter_es/* LibroJupyterConfiguration */.WLy.AllowDownload, true);
              this.configurationService.set(libro_jupyter_es/* LibroJupyterConfiguration */.WLy.AllowUpload, true);
              this.fileCommandContribution.allowUpload = true;
              this.fileCommandContribution.allowDownload = true;
              baseUrl = libro_jupyter_es/* PageConfig */.Pzp.getOption('baseUrl');
              el = document.getElementById('jupyter-config-data');
              if (el) {
                pageConfig = JSON.parse(el.textContent || '');
                baseUrl = pageConfig['baseUrl'];
                if (baseUrl && baseUrl.startsWith('/')) {
                  baseUrl = window.location.origin + baseUrl;
                }
              }
              localStorage.setItem(ShouldPreventStoreViewKey, 'true');
              this.configurationService.set(libro_jupyter_es/* LibroJupyterConfiguration */.WLy['OpenSlot'], es/* LibroLabLayoutSlots */.uRJ.content);
              this.configurationService.set(libro_terminal_es/* terminalDefaultSlot */.I$, es/* LibroLabLayoutSlots */.uRJ.contentBottom);
              this.serverConnection.updateSettings({
                baseUrl: baseUrl,
                wsUrl: baseUrl.replace(/^http(s)?/, 'ws$1')
              });
              this.serverManager.launch();
              this.serverManager.ready.then( /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
                var defaultOpenUri;
                return regeneratorRuntime_default()().wrap(function _callee$(_context) {
                  while (1) switch (_context.prev = _context.next) {
                    case 0:
                      _this.layoutService.setAreaVisible(es/* LibroLabLayoutSlots */.uRJ.navigator, true);
                      _this.layoutService.setAreaVisible(es/* LibroLabLayoutSlots */.uRJ.alert, false);
                      _this.layoutService.serverSatus = 'success';
                      _context.next = 5;
                      return _this.initialWorkspace();
                    case 5:
                      if (_this.location) {
                        defaultOpenUri = new uri/* URI */.o(_this.location + '/__init__.py');
                        _this.openerService.getOpener(defaultOpenUri).then(function (opener) {
                          if (opener) {
                            opener.open(defaultOpenUri, {
                              viewOptions: {
                                name: '__init__.py'
                              }
                            });
                          }
                        });
                      }
                      return _context.abrupt("return");
                    case 7:
                    case "end":
                      return _context.stop();
                  }
                }, _callee);
              })))["catch"](console.error);
            case 13:
            case "end":
              return _context2.stop();
          }
        }, _callee2, this);
      }));
      function onStart() {
        return _onStart.apply(this, arguments);
      }
      return onStart;
    }()
  }, {
    key: "initialWorkspace",
    value: function () {
      var _initialWorkspace = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee3() {
        var _res$data;
        var queryParams, flow_uid, res, view, _res$data2, location;
        return regeneratorRuntime_default()().wrap(function _callee3$(_context3) {
          while (1) switch (_context3.prev = _context3.next) {
            case 0:
              queryParams = query_string/* default */.Z.parse(window.location.search);
              flow_uid = queryParams['flow_uid'];
              _context3.next = 4;
              return this.fetcher.get("/api/v1/serve/awel/flow/notebook/file/path", {
                flow_uid: flow_uid
              }, {
                baseURL: 'http://localhost:5670'
              });
            case 4:
              res = _context3.sent;
              if (!(res.status && (_res$data = res.data) !== null && _res$data !== void 0 && (_res$data = _res$data.data) !== null && _res$data !== void 0 && _res$data.path)) {
                _context3.next = 10;
                break;
              }
              _context3.next = 8;
              return this.viewManager.getOrCreateView(file_tree_view/* FileTreeViewFactory */.y6);
            case 8:
              view = _context3.sent;
              if (view) {
                location = (_res$data2 = res.data) === null || _res$data2 === void 0 || (_res$data2 = _res$data2.data) === null || _res$data2 === void 0 ? void 0 : _res$data2.path;
                this.location = location;
                view.model.rootVisible = false;
                view.model.location = new uri/* URI */.o(location);
              }
            case 10:
            case "end":
              return _context3.stop();
          }
        }, _callee3, this);
      }));
      function initialWorkspace() {
        return _initialWorkspace.apply(this, arguments);
      }
      return initialWorkspace;
    }()
  }]);
  return LibroApp;
}(), (_descriptor = applyDecoratedDescriptor_default()(_class2.prototype, "serverConnection", [_dec2], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor2 = applyDecoratedDescriptor_default()(_class2.prototype, "serverManager", [_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor3 = applyDecoratedDescriptor_default()(_class2.prototype, "viewManager", [_dec4], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor4 = applyDecoratedDescriptor_default()(_class2.prototype, "slotViewManager", [_dec5], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor5 = applyDecoratedDescriptor_default()(_class2.prototype, "configurationService", [_dec6], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor6 = applyDecoratedDescriptor_default()(_class2.prototype, "layoutService", [_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor7 = applyDecoratedDescriptor_default()(_class2.prototype, "fileCommandContribution", [_dec8], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor8 = applyDecoratedDescriptor_default()(_class2.prototype, "fetcher", [_dec9], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor9 = applyDecoratedDescriptor_default()(_class2.prototype, "openerService", [_dec10], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor10 = applyDecoratedDescriptor_default()(_class2.prototype, "libroFileService", [_dec11], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), _class2)) || _class);
;// CONCATENATED MODULE: ./src/pages/dbgpt/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/inherits.js
var inherits = __webpack_require__(31996);
var inherits_default = /*#__PURE__*/__webpack_require__.n(inherits);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createSuper.js
var createSuper = __webpack_require__(26037);
var createSuper_default = /*#__PURE__*/__webpack_require__.n(createSuper);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-prompt-cell/es/index.js + 26 modules
var libro_prompt_cell_es = __webpack_require__(32663);
;// CONCATENATED MODULE: ./src/pages/dbgpt/prompt-script.ts




var prompt_script_dec, prompt_script_class;


var LibroPromptScript = (prompt_script_dec = (0,mana_syringe_es/* singleton */.ri)(), prompt_script_dec(prompt_script_class = /*#__PURE__*/function (_PromptScript) {
  inherits_default()(LibroPromptScript, _PromptScript);
  var _super = createSuper_default()(LibroPromptScript);
  function LibroPromptScript() {
    var _this;
    classCallCheck_default()(this, LibroPromptScript);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.getChatObjects = "from libro_ai import chat_object_manager\nchat_object_manager.dump_kernel_list_json()";
    _this.getChatRecoreds = "from libro_ai import chat_record_provider\nchat_record_provider.get_records()";
    return _this;
  }
  return createClass_default()(LibroPromptScript);
}(libro_prompt_cell_es/* PromptScript */.rH)) || prompt_script_class);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/assertThisInitialized.js
var assertThisInitialized = __webpack_require__(25098);
var assertThisInitialized_default = /*#__PURE__*/__webpack_require__.n(assertThisInitialized);
// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(67294);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-observable/es/index.js + 12 modules
var mana_observable_es = __webpack_require__(94725);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-protocol.js
var view_protocol = __webpack_require__(45573);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/decorator.js
var decorator = __webpack_require__(64424);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-core/es/index.js + 313 modules
var libro_core_es = __webpack_require__(99822);
// EXTERNAL MODULE: ./node_modules/@rjsf/antd/lib/index.js + 85 modules
var lib = __webpack_require__(30112);
// EXTERNAL MODULE: ./node_modules/@rjsf/validator-ajv8/lib/index.js + 6 modules
var validator_ajv8_lib = __webpack_require__(74717);
;// CONCATENATED MODULE: ./src/pages/dbgpt/schema-form-widget/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/react/jsx-runtime.js
var jsx_runtime = __webpack_require__(85893);
;// CONCATENATED MODULE: ./src/pages/dbgpt/schema-form-widget/view.tsx








var view_dec, view_dec2, view_dec3, view_class, view_class2, view_descriptor;









function SubmitButton(props) {
  return null;
}
var LibroSchemaFormWidgetComponent = /*#__PURE__*/(0,react.forwardRef)(function (props, ref) {
  var widgetView = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var formRef = (0,react.useRef)(null);
  var schema = (0,react.useMemo)(function () {
    try {
      return JSON.parse(widgetView.schema);
    } catch (e) {
      return {};
    }
  }, [widgetView.schema]);
  var value = (0,react.useMemo)(function () {
    try {
      var v = JSON.parse(widgetView.value);
      if (formRef.current) {
        formRef.current.setState(v);
      }
      return v;
    } catch (e) {
      // console.error(e);
      return {};
    }
  }, [widgetView.value]);
  var handleChange = (0,react.useCallback)(function (values) {
    var data = {
      buffer_paths: [],
      method: 'update',
      state: {
        value: JSON.stringify(values.formData)
      }
    };
    widgetView.send(data);
  }, [widgetView]);
  if (widgetView.isCommClosed) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-widget-schema-form",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(lib/* default */.ZP, {
      ref: formRef,
      schema: schema,
      validator: validator_ajv8_lib/* default */.ZP,
      onChange: handleChange,
      templates: {
        ButtonTemplates: {
          SubmitButton: SubmitButton
        }
      }
    })
  });
});
var LibroSchemaFormtWidget = (view_dec = (0,mana_syringe_es/* transient */.H3)(), view_dec2 = (0,decorator/* view */.ei)('libro-widget-schema-form-view'), view_dec3 = (0,mana_observable_es/* prop */.vg)(), view_dec(view_class = view_dec2(view_class = (view_class2 = /*#__PURE__*/function (_WidgetView) {
  inherits_default()(LibroSchemaFormtWidget, _WidgetView);
  var _super = createSuper_default()(LibroSchemaFormtWidget);
  function LibroSchemaFormtWidget(props, libroContextKey) {
    var _this;
    classCallCheck_default()(this, LibroSchemaFormtWidget);
    _this = _super.call(this, props, libroContextKey);
    _this.view = LibroSchemaFormWidgetComponent;
    _this.schema = void 0;
    initializerDefineProperty_default()(_this, "value", view_descriptor, assertThisInitialized_default()(_this));
    _this.schema = props.attributes.schema;
    _this.value = props.attributes.value;
    return _this;
  }
  LibroSchemaFormtWidget = (0,mana_syringe_es/* inject */.f3)(libro_core_es/* LibroContextKey */.z4)(LibroSchemaFormtWidget, undefined, 1) || LibroSchemaFormtWidget;
  LibroSchemaFormtWidget = (0,mana_syringe_es/* inject */.f3)(view_protocol/* ViewOption */.Hj)(LibroSchemaFormtWidget, undefined, 0) || LibroSchemaFormtWidget;
  createClass_default()(LibroSchemaFormtWidget, [{
    key: "handleCommMsg",
    value: function handleCommMsg(msg) {
      var data = msg.content.data;
      var method = data.method;
      switch (method) {
        case 'update':
        case 'echo_update':
          if (data.state.value) {
            this.value = data.state.value;
          }
          if (data.state.schema) {
            this.schema = data.state.schema;
          }
      }
      return Promise.resolve();
    }
  }]);
  return LibroSchemaFormtWidget;
}(libro_jupyter_es/* WidgetView */.LfK), (view_descriptor = applyDecoratedDescriptor_default()(view_class2.prototype, "value", [view_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), view_class2)) || view_class) || view_class);
;// CONCATENATED MODULE: ./src/pages/dbgpt/schema-form-widget/contribution.ts





var contribution_dec, contribution_dec2, contribution_class, contribution_class2, contribution_descriptor;



var SchemaFormModelContribution = (contribution_dec = (0,mana_syringe_es/* singleton */.ri)({
  contrib: libro_jupyter_es/* WidgetViewContribution */.roO
}), contribution_dec2 = (0,mana_syringe_es/* inject */.f3)(view_manager/* ViewManager */.v), contribution_dec(contribution_class = (contribution_class2 = /*#__PURE__*/function () {
  function SchemaFormModelContribution() {
    classCallCheck_default()(this, SchemaFormModelContribution);
    initializerDefineProperty_default()(this, "viewManager", contribution_descriptor, this);
    this.canHandle = function (attributes) {
      if (attributes._model_name === 'SchemaFormModel') {
        return 100;
      }
      return 1;
    };
  }
  createClass_default()(SchemaFormModelContribution, [{
    key: "factory",
    value: function factory(props) {
      return this.viewManager.getOrCreateView(LibroSchemaFormtWidget, props);
    }
  }]);
  return SchemaFormModelContribution;
}(), (contribution_descriptor = applyDecoratedDescriptor_default()(contribution_class2.prototype, "viewManager", [contribution_dec2], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), contribution_class2)) || contribution_class);
;// CONCATENATED MODULE: ./src/pages/dbgpt/schema-form-widget/index.ts




var LibroSchemaFormWidgetModule = mana_module/* ManaModule */.R.create().register(LibroSchemaFormtWidget, SchemaFormModelContribution).dependOn(libro_jupyter_es/* WidgetModule */.yF7);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot.js
var slot = __webpack_require__(42681);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-l10n/es/index.js + 4 modules
var mana_l10n_es = __webpack_require__(84863);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-react/es/index.js + 84 modules
var mana_react_es = __webpack_require__(25087);
// EXTERNAL MODULE: ./node_modules/antd/es/alert/index.js + 4 modules
var es_alert = __webpack_require__(40056);
;// CONCATENATED MODULE: ./src/pages/dbgpt/dbgbt-layout.tsx




var dbgbt_layout_dec, dbgbt_layout_dec2, dbgbt_layout_class;








var LibroDbgptLayoutComponent = /*#__PURE__*/(0,react.forwardRef)(function LibroLabLayoutComponent() {
  var layoutService = (0,mana_observable_es/* useInject */.oC)(es/* LayoutService */.Pb3);
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-lab-layout",
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)(mana_react_es/* BoxPanel */.jN, {
      direction: "top-to-bottom",
      children: [layoutService.isAreaVisible(es/* LibroLabLayoutSlots */.uRJ.alert) && /*#__PURE__*/(0,jsx_runtime.jsx)(es_alert/* default */.Z, {
        message: mana_l10n_es/* l10n */.U6.t('服务启动中，请稍后，待服务启动完成后即可编辑文件。'),
        type: "info",
        banner: true,
        closable: true,
        icon: /*#__PURE__*/(0,jsx_runtime.jsx)(es/* Loadding */.SW0, {
          className: "libro-lab-loadding"
        })
      }), layoutService.isAreaVisible(es/* LibroLabLayoutSlots */.uRJ.container) && /*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-lab-layout-container",
        flex: 1,
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(slot/* Slot */.g, {
          name: es/* LibroLabLayoutSlots */.uRJ.container
        })
      })]
    })
  }, layoutService.refreshKey);
});
var LibroDbgptLayoutView = (dbgbt_layout_dec = (0,mana_syringe_es/* singleton */.ri)(), dbgbt_layout_dec2 = (0,decorator/* view */.ei)('libro-lab-layout'), dbgbt_layout_dec(dbgbt_layout_class = dbgbt_layout_dec2(dbgbt_layout_class = /*#__PURE__*/function (_LibroLabLayoutView) {
  inherits_default()(LibroDbgptLayoutView, _LibroLabLayoutView);
  var _super = createSuper_default()(LibroDbgptLayoutView);
  function LibroDbgptLayoutView() {
    var _this;
    classCallCheck_default()(this, LibroDbgptLayoutView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = LibroDbgptLayoutComponent;
    return _this;
  }
  return createClass_default()(LibroDbgptLayoutView);
}(es/* LibroLabLayoutView */.lUv)) || dbgbt_layout_class) || dbgbt_layout_class);
;// CONCATENATED MODULE: ./src/pages/dbgpt/logo.tsx


var Logo = function Logo() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("svg", {
    width: "20px",
    height: "20px",
    viewBox: "0 0 154 116",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("g", {
      id: "\u9875\u9762-1",
      stroke: "none",
      "stroke-width": "1",
      fill: "none",
      "fill-rule": "evenodd",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("g", {
        id: "\u753B\u677F\u5907\u4EFD-6",
        transform: "translate(-119.000000, -152.000000)",
        children: /*#__PURE__*/(0,jsx_runtime.jsxs)("g", {
          id: "Libro-logo",
          transform: "translate(119.000000, 152.000000)",
          children: [/*#__PURE__*/(0,jsx_runtime.jsx)("path", {
            d: "M128.970588,66 C142.793951,66 154,77.1926795 154,90.9995493 C154,104.806419 142.793951,115.999099 128.970588,115.999099 C128.473758,115.999099 127.980309,115.98464 127.49064,115.956121 L127.697007,115.999674 L80,115.999099 L93.1090651,98.1074032 L108.158627,77.1069733 C112.649045,70.4093826 120.294268,66 128.970588,66 Z",
            id: "\u5F62\u72B6\u7ED3\u5408",
            fill: "#155DE2"
          }), /*#__PURE__*/(0,jsx_runtime.jsx)("path", {
            d: "M104.481034,0 L147,0 L147,0 L59.3397468,116 L0,116 L78.0248494,13.1382037 C84.3029962,4.8615911 94.0927023,-5.19712172e-15 104.481034,0 Z",
            id: "\u77E9\u5F62",
            fill: "#155DE2"
          }), /*#__PURE__*/(0,jsx_runtime.jsx)("path", {
            d: "M65.667264,51.1430655 C65.667264,84.8453007 91.2203312,112.576275 123.999729,115.999972 L0,115.997535 L75.3014571,17.0042341 C69.1915639,26.9341621 65.667264,38.6268332 65.667264,51.1430655 Z",
            id: "\u5F62\u72B6\u7ED3\u5408",
            fill: "#12D8C6"
          })]
        })
      })
    })
  });
};
// EXTERNAL MODULE: ./node_modules/antd/es/tooltip/index.js + 3 modules
var tooltip = __webpack_require__(83062);
;// CONCATENATED MODULE: ./src/pages/dbgpt/dbgpt-current-file-footer-view.tsx




var dbgpt_current_file_footer_view_dec, dbgpt_current_file_footer_view_dec2, dbgpt_current_file_footer_view_class;









var DbgptCurrentFileFooterComponent = /*#__PURE__*/react.forwardRef(function CurrentFileFooterComponent(_props, ref) {
  var _currentFileFooterVie;
  var currentFileFooterView = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var label = (_currentFileFooterVie = currentFileFooterView.navigatableView) === null || _currentFileFooterVie === void 0 ? void 0 : _currentFileFooterVie.title.label;
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-lab-current-file-footer",
    ref: ref,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(tooltip/* default */.Z, {
      title: "\u70B9\u51FB\u8DF3\u8F6C libro",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("span", {
        onClick: function onClick() {
          window.open('https://github.com/difizen/libro', '_blank');
        },
        className: "libro-dbgpt-footer-logo",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(Logo, {})
      })
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("span", {
      children: mana_l10n_es/* l10n */.U6.t('当前文件：')
    }), typeof label === 'function' ? /*#__PURE__*/react.createElement(label) // 如果是 React.FC，调用它
    : label /* 如果是 ReactNode，直接渲染 */]
  });
});
var LibroDbgptLabCurrentFileFooterView = (dbgpt_current_file_footer_view_dec = (0,mana_syringe_es/* singleton */.ri)(), dbgpt_current_file_footer_view_dec2 = (0,decorator/* view */.ei)('libro-lab-current-file-footer-view'), dbgpt_current_file_footer_view_dec(dbgpt_current_file_footer_view_class = dbgpt_current_file_footer_view_dec2(dbgpt_current_file_footer_view_class = /*#__PURE__*/function (_LibroLabCurrentFileF) {
  inherits_default()(LibroDbgptLabCurrentFileFooterView, _LibroLabCurrentFileF);
  var _super = createSuper_default()(LibroDbgptLabCurrentFileFooterView);
  function LibroDbgptLabCurrentFileFooterView() {
    var _this;
    classCallCheck_default()(this, LibroDbgptLabCurrentFileFooterView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = DbgptCurrentFileFooterComponent;
    return _this;
  }
  return createClass_default()(LibroDbgptLabCurrentFileFooterView);
}(es/* LibroLabCurrentFileFooterView */.gfc)) || dbgpt_current_file_footer_view_class) || dbgpt_current_file_footer_view_class);
;// CONCATENATED MODULE: ./src/pages/dbgpt/index.tsx










var BaseModule = mana_module/* ManaModule */.R.create().register({
  token: es/* LibroLabApp */.QFc,
  useClass: LibroApp
}, {
  token: libro_prompt_cell_es/* PromptScript */.rH,
  useClass: LibroPromptScript,
  lifecycle: mana_syringe_es/* Syringe */.J3.Lifecycle.singleton
}, {
  token: es/* LibroLabLayoutView */.lUv,
  useClass: LibroDbgptLayoutView
}, {
  token: es/* LibroLabCurrentFileFooterView */.gfc,
  useClass: LibroDbgptLabCurrentFileFooterView
});
var App = function App() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-workbench-app",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(components/* ManaComponents */.rF.Application, {
      asChild: true,
      modules: [mana_app_es/* ManaAppPreset */.n6L, es/* LibroLabModule */.knY, BaseModule, LibroSchemaFormWidgetModule]
    }, "libro")
  });
};
/* harmony default export */ var dbgpt = (App);

/***/ }),

/***/ 22868:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 14777:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 99830:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 70209:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 87414:
/***/ (function() {

/* (ignored) */

/***/ })

}]);