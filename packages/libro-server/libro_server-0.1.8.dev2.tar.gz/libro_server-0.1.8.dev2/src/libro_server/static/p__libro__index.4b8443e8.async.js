(self["webpackChunklibro_lab"] = self["webpackChunklibro_lab"] || []).push([[119],{

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

/***/ 34623:
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": function() { return /* binding */ libro; }
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
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot-view-manager.js
var slot_view_manager = __webpack_require__(94104);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/application/application.js
var application = __webpack_require__(15910);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-manager.js
var view_manager = __webpack_require__(44659);
;// CONCATENATED MODULE: ./src/pages/libro/app.ts







var _dec, _dec2, _dec3, _dec4, _dec5, _dec6, _dec7, _class, _class2, _descriptor, _descriptor2, _descriptor3, _descriptor4, _descriptor5, _descriptor6;





var LibroApp = (_dec = (0,mana_syringe_es/* singleton */.ri)({
  contrib: application/* ApplicationContribution */.rS
}), _dec2 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), _dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerManager */.ErZ), _dec4 = (0,mana_syringe_es/* inject */.f3)(view_manager/* ViewManager */.v), _dec5 = (0,mana_syringe_es/* inject */.f3)(slot_view_manager/* SlotViewManager */.I), _dec6 = (0,mana_syringe_es/* inject */.f3)(configuration_service/* ConfigurationService */.e), _dec7 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* FileCommandContribution */.uq5), _dec(_class = (_class2 = /*#__PURE__*/function () {
  function LibroApp() {
    classCallCheck_default()(this, LibroApp);
    initializerDefineProperty_default()(this, "serverConnection", _descriptor, this);
    initializerDefineProperty_default()(this, "serverManager", _descriptor2, this);
    initializerDefineProperty_default()(this, "viewManager", _descriptor3, this);
    initializerDefineProperty_default()(this, "slotViewManager", _descriptor4, this);
    initializerDefineProperty_default()(this, "configurationService", _descriptor5, this);
    initializerDefineProperty_default()(this, "fileCommandContribution", _descriptor6, this);
  }
  createClass_default()(LibroApp, [{
    key: "onStart",
    value: function () {
      var _onStart = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
        var baseUrl, el, pageConfig;
        return regeneratorRuntime_default()().wrap(function _callee$(_context) {
          while (1) switch (_context.prev = _context.next) {
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
              this.serverConnection.updateSettings({
                baseUrl: baseUrl,
                wsUrl: baseUrl.replace(/^http(s)?/, 'ws$1')
              });
              this.serverManager.launch();
            case 9:
            case "end":
              return _context.stop();
          }
        }, _callee, this);
      }));
      function onStart() {
        return _onStart.apply(this, arguments);
      }
      return onStart;
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
}), _descriptor6 = applyDecoratedDescriptor_default()(_class2.prototype, "fileCommandContribution", [_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), _class2)) || _class);
;// CONCATENATED MODULE: ./src/pages/libro/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/inherits.js
var inherits = __webpack_require__(31996);
var inherits_default = /*#__PURE__*/__webpack_require__.n(inherits);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createSuper.js
var createSuper = __webpack_require__(26037);
var createSuper_default = /*#__PURE__*/__webpack_require__.n(createSuper);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-prompt-cell/es/index.js + 26 modules
var libro_prompt_cell_es = __webpack_require__(32663);
;// CONCATENATED MODULE: ./src/pages/libro/prompt-script.ts




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
;// CONCATENATED MODULE: ./src/pages/libro/schema-form-widget/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/react/jsx-runtime.js
var jsx_runtime = __webpack_require__(85893);
;// CONCATENATED MODULE: ./src/pages/libro/schema-form-widget/view.tsx








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
;// CONCATENATED MODULE: ./src/pages/libro/schema-form-widget/contribution.ts





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
;// CONCATENATED MODULE: ./src/pages/libro/schema-form-widget/index.ts




var LibroSchemaFormWidgetModule = mana_module/* ManaModule */.R.create().register(LibroSchemaFormtWidget, SchemaFormModelContribution).dependOn(libro_jupyter_es/* WidgetModule */.yF7);
;// CONCATENATED MODULE: ./src/pages/libro/index.tsx








var BaseModule = mana_module/* ManaModule */.R.create().register(LibroApp, {
  token: libro_prompt_cell_es/* PromptScript */.rH,
  useClass: LibroPromptScript,
  lifecycle: mana_syringe_es/* Syringe */.J3.Lifecycle.singleton
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
/* harmony default export */ var libro = (App);

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