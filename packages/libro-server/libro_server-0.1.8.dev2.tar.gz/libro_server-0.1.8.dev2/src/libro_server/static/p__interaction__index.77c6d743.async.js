(self["webpackChunklibro_lab"] = self["webpackChunklibro_lab"] || []).push([[576],{

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

/***/ 18737:
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": function() { return /* binding */ interaction; }
});

// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/module/mana-module.js
var mana_module = __webpack_require__(17354);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/decorator.js
var decorator = __webpack_require__(64424);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-protocol.js
var view_protocol = __webpack_require__(45573);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/view/header/header-view.js + 1 modules
var header_view = __webpack_require__(92072);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/components/index.js + 6 modules
var components = __webpack_require__(10533);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/index.js + 45 modules
var es = __webpack_require__(77780);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-lab/es/index.js + 400 modules
var libro_lab_es = __webpack_require__(46348);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-jupyter/es/index.js + 430 modules
var libro_jupyter_es = __webpack_require__(52638);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-widget/es/index.js + 8 modules
var libro_widget_es = __webpack_require__(34179);
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
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/configuration/configuration-service.js
var configuration_service = __webpack_require__(52243);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot-view-manager.js
var slot_view_manager = __webpack_require__(94104);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/application/application.js
var application = __webpack_require__(15910);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-manager.js
var view_manager = __webpack_require__(44659);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-syringe/es/index.js + 15 modules
var mana_syringe_es = __webpack_require__(49383);
;// CONCATENATED MODULE: ./src/pages/interaction/app.ts







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
              document.title = "libro execution";
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
            case 10:
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
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/assertThisInitialized.js
var assertThisInitialized = __webpack_require__(25098);
var assertThisInitialized_default = /*#__PURE__*/__webpack_require__.n(assertThisInitialized);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/inherits.js
var inherits = __webpack_require__(31996);
var inherits_default = /*#__PURE__*/__webpack_require__.n(inherits);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createSuper.js
var createSuper = __webpack_require__(26037);
var createSuper_default = /*#__PURE__*/__webpack_require__.n(createSuper);
// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(67294);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-observable/es/index.js + 12 modules
var mana_observable_es = __webpack_require__(94725);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-render.js
var view_render = __webpack_require__(41814);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/default-view.js + 1 modules
var default_view = __webpack_require__(58304);
// EXTERNAL MODULE: ./node_modules/query-string/index.js + 1 modules
var query_string = __webpack_require__(87449);
// EXTERNAL MODULE: ./node_modules/antd/es/spin/index.js + 6 modules
var spin = __webpack_require__(74330);
// EXTERNAL MODULE: ./node_modules/antd/es/radio/index.js + 5 modules
var es_radio = __webpack_require__(78045);
;// CONCATENATED MODULE: ./src/pages/interaction/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/objectSpread2.js
var objectSpread2 = __webpack_require__(97857);
var objectSpread2_default = /*#__PURE__*/__webpack_require__.n(objectSpread2);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/objectWithoutProperties.js
var objectWithoutProperties = __webpack_require__(13769);
var objectWithoutProperties_default = /*#__PURE__*/__webpack_require__.n(objectWithoutProperties);
// EXTERNAL MODULE: ./node_modules/antd/es/button/index.js + 27 modules
var es_button = __webpack_require__(73318);
// EXTERNAL MODULE: ./node_modules/antd/es/back-top/index.js + 1 modules
var back_top = __webpack_require__(80093);
// EXTERNAL MODULE: ./node_modules/@ant-design/icons/es/icons/ToTopOutlined.js + 1 modules
var ToTopOutlined = __webpack_require__(75162);
// EXTERNAL MODULE: ./node_modules/classnames/index.js
var classnames = __webpack_require__(93967);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/slicedToArray.js
var slicedToArray = __webpack_require__(5574);
var slicedToArray_default = /*#__PURE__*/__webpack_require__.n(slicedToArray);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/typeof.js
var helpers_typeof = __webpack_require__(52677);
var typeof_default = /*#__PURE__*/__webpack_require__.n(helpers_typeof);
// EXTERNAL MODULE: ./node_modules/resize-observer-polyfill/dist/ResizeObserver.es.js
var ResizeObserver_es = __webpack_require__(91033);
// EXTERNAL MODULE: ./node_modules/react/jsx-runtime.js
var jsx_runtime = __webpack_require__(85893);
;// CONCATENATED MODULE: ./src/pages/interaction/default-dnd-content.tsx


/* eslint-disable react-hooks/exhaustive-deps */






var AppCellContainer = function AppCellContainer(_ref) {
  var cell = _ref.cell,
    index = _ref.index;
  var ref = (0,react.useRef)(null);
  var appInstance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var instance = appInstance.libroView;
  var cellService = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* LibroCellService */.lt3);
  (0,react.useLayoutEffect)(function () {
    if (typeof_default()(ref) !== 'object') {
      return function () {
        //
      };
    }
    var el = ref === null || ref === void 0 ? void 0 : ref.current;
    if (!el) {
      return function () {
        //
      };
    }
    var resizeObserver = new ResizeObserver(function (entries) {
      entries.forEach(function (entry) {
        var isVisible = entry.contentRect.width !== 0 && entry.contentRect.height !== 0;
        if (isVisible) {
          var _ref$current;
          cell.noEditorAreaHeight = ((_ref$current = ref.current) === null || _ref$current === void 0 ? void 0 : _ref$current.clientHeight) || 0;
        }
      });
    });
    resizeObserver.observe(el);
    return function () {
      cell.noEditorAreaHeight = 0;
      resizeObserver.disconnect();
    };
  }, [ref, cell]);
  var handleFocus = (0,react.useCallback)(function (e) {
    if (!instance) return;
    var className = e.target.className;
    if (e.target.tagName === 'svg' || className && className && typeof className === 'string' && (className.includes('mana-toolbar-item') || className.includes('mana-toolbar'))) {
      return;
    }
    instance.model.selectCell(cell);
    instance.model.selections = [];
    if (cell.shouldEnterEditorMode(e)) {
      instance.enterEditMode();
    }
  }, [instance, cell]);
  var handleMouseDown = (0,react.useCallback)(function (e) {
    if (!instance) return;
    instance.model.mouseMode = 'mouseDown';
  }, [instance, index]);
  var handleMouseUp = (0,react.useCallback)(function () {
    if (!instance) return;
    if (instance.model.mouseMode === 'multipleSelection' || instance.model.mouseMode === 'drag') {
      return;
    }
    instance.model.selectCell(cell);
    instance.model.selections = [];
  }, [instance, cell]);
  var opacity = 1;
  if (!instance) return null;
  var ItemRender = (0,mana_observable_es/* getOrigin */.P$)(appInstance.dndItemRender);
  var isMultiSelected = instance.model.selections.length !== 0 && instance.isSelected(cell);
  // let isMouseOver = false;
  var _useState = (0,react.useState)(false),
    _useState2 = slicedToArray_default()(_useState, 2),
    isMouseOverDragArea = _useState2[0],
    setIsMouseOverDragArea = _useState2[1];
  var hasCellHidden = (0,react.useMemo)(function () {
    return cell.hasCellHidden();
  }, [cell]);
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-dnd-cell-container ".concat(isMultiSelected ? 'multi-selected' : '', " ").concat(hasCellHidden ? 'hidden' : ''),
    style: {
      opacity: opacity
    },
    ref: ref,
    id: cell.id,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-drag-area",
      onMouseDown: handleMouseDown,
      onMouseUp: handleMouseUp,
      onMouseOver: function onMouseOver() {
        return setIsMouseOverDragArea(true);
      },
      onMouseLeave: function onMouseLeave() {
        return setIsMouseOverDragArea(false);
      }
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      tabIndex: -1,
      onFocus: handleFocus
      // onClick={e => e.preventDefault()}
      ,
      className: "libro-dnd-cell-content",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(ItemRender, {
        isDragOver: false,
        isDrag: false,
        cell: cell,
        isMouseOverDragArea: isMouseOverDragArea
      })
    })]
  });
};
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/configuration/hooks.js
var hooks = __webpack_require__(13684);
;// CONCATENATED MODULE: ./src/pages/interaction/dnd-cell-item-render.tsx

/* eslint-disable react-hooks/exhaustive-deps */






var CellInputContent = /*#__PURE__*/(0,react.memo)(function CellInputContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var CellExecutionTime = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellExecutionTimeProvider */.fyr);
  var CellInputBottonBlank = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellInputBottonBlankProvider */.$iz);
  if (!(observableCell !== null && observableCell !== void 0 && observableCell.view) || !(0,libro_jupyter_es/* isCellView */.CZ3)(observableCell)) {
    return null;
  }
  var isHidden = observableCell.hasInputHidden;
  if (isHidden) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-input-hidden",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(libro_jupyter_es/* ContentMore */.eoC, {})
    });
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-cell-input-content",
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(CellExecutionTime, {
      cell: cell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
      view: observableCell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(CellInputBottonBlank, {
      cell: cell
    })]
  });
});
var CellInputInnner = /*#__PURE__*/(0,react.forwardRef)(function CellInput(props, ref) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var _useConfigurationValu = (0,hooks/* useConfigurationValue */.K)(libro_jupyter_es/* CollapserClickActive */.gfq),
    _useConfigurationValu2 = slicedToArray_default()(_useConfigurationValu, 1),
    collapserClickActive = _useConfigurationValu2[0];
  var handleCellInputCollapser = function handleCellInputCollapser() {
    if (collapserClickActive) {
      observableCell.hasInputHidden = !observableCell.hasInputHidden;
    }
  };
  // TODO: 性能！
  // const isFirstCell = cell.parent.model.cells.indexOf(cell) === 0 ? true : false;
  var isFirstCell = (0,react.useMemo)(function () {
    return observableCell.parent.model.cells[0] && (0,mana_observable_es/* equals */.fS)(observableCell.parent.model.cells[0], observableCell) ? true : false;
  }, [observableCell]);
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-cell-container",
    tabIndex: 10,
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(CellInputContent, {
      cell: observableCell
    })
  });
});
var CellInput = /*#__PURE__*/(0,react.memo)(CellInputInnner);
var CellOutputContent = /*#__PURE__*/(0,react.memo)(function CellOutputContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var CellOutputVisulization = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellOutputVisulizationProvider */.hdu);
  if (!libro_jupyter_es/* ExecutableCellView */.q0L.is(cell) || !libro_jupyter_es/* ExecutableCellView */.q0L.is(observableCell)) {
    return null;
  }
  if (!libro_jupyter_es/* ExecutableCellModel */.oM$.is(observableCell.model)) {
    return null;
  }
  var hasOutputsScrolled = observableCell.model.hasOutputsScrolled;
  var isHidden = observableCell.model.hasOutputHidden;
  if (isHidden) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-cell-output-hidden",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(libro_jupyter_es/* ContentMore */.eoC, {})
    });
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-cell-output-content ".concat(hasOutputsScrolled ? 'scrolled' : '', " "),
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(CellOutputVisulization, {
      cell: cell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
      view: cell.outputArea
    })]
  });
});
var LibroCellExecutionTime = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellExecutionTime() {
  return null;
})));
var LibroCellInputBottonBlank = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellInputBottonBlank() {
  return null;
})));
var LibroCellVisualization = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellVisualization() {
  return null;
})));
var CellOutput = /*#__PURE__*/(0,react.forwardRef)(function CellOutput(props, ref) {
  var _cell$outputArea;
  var cell = props.cell;
  var outputRef = (0,react.useRef)(null);
  var isExecutingRef = (0,react.useRef)(null);
  var executing = false;
  if (libro_jupyter_es/* ExecutableCellModel */.oM$.is(cell.model)) {
    executing = cell.model.executing;
  }
  (0,react.useLayoutEffect)(function () {
    isExecutingRef.current = !!executing;
  }, [executing]);
  if (!libro_jupyter_es/* ExecutableCellView */.q0L.is(cell)) {
    return null;
  }
  if (!(0,libro_jupyter_es/* isCellView */.CZ3)(cell) || !libro_jupyter_es/* ExecutableCellModel */.oM$.is(cell.model) || !((_cell$outputArea = cell.outputArea) !== null && _cell$outputArea !== void 0 && _cell$outputArea.length)) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-cell-output-container",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      ref: outputRef,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(CellOutputContent, {
        cell: cell
      })
    })
  });
});
var DndCellItemContent = /*#__PURE__*/(0,react.memo)(function DndCellItemContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  if (cell.model.type === 'markdown') {
    return /*#__PURE__*/(0,jsx_runtime.jsx)(CellInput, {
      cell: observableCell
    });
  } else {
    return /*#__PURE__*/(0,jsx_runtime.jsx)(CellOutput, {
      cell: observableCell
    });
  }
});
var DndCellItemRenderInner = /*#__PURE__*/(0,react.forwardRef)(function DndCellItemRender(props, ref) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var appInstance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var instance = appInstance.libroView;
  var hasErrorOutputs = (0,libro_jupyter_es/* hasErrorOutput */.DJ7)(observableCell);
  var hasCellHidden = (0,react.useMemo)(function () {
    return observableCell.hasCellHidden();
  }, [observableCell]);
  var classNames = ['libro-dnd-cell', {
    'command-mode': instance === null || instance === void 0 ? void 0 : instance.model.commandMode
  }, {
    'edit-mode': !(instance !== null && instance !== void 0 && instance.model.commandMode)
  }, {
    error: hasErrorOutputs
  }, {
    hidden: hasCellHidden
  }];
  if (observableCell.wrapperCls) {
    classNames.push(observableCell.wrapperCls);
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-dnd-cell-border",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: classnames_default()(classNames),
      ref: ref,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellItemContent, {
        cell: cell
      })
    })
  });
});
var DndCellItemRender = /*#__PURE__*/(0,react.memo)(DndCellItemRenderInner);
;// CONCATENATED MODULE: ./src/pages/interaction/libro-app-view.tsx












var libro_app_view_dec, libro_app_view_dec2, libro_app_view_dec3, libro_app_view_dec4, libro_app_view_dec5, libro_app_view_dec6, libro_app_view_dec7, _dec8, libro_app_view_class, libro_app_view_class2, libro_app_view_descriptor, libro_app_view_descriptor2, libro_app_view_descriptor3, libro_app_view_descriptor4, libro_app_view_descriptor5, libro_app_view_descriptor6;
var _excluded = ["cell", "index"];













var DndCellRender = /*#__PURE__*/(0,react.memo)(function DndCellRender(_ref) {
  var cell = _ref.cell,
    index = _ref.index,
    props = objectWithoutProperties_default()(_ref, _excluded);
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var appInstance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var instance = appInstance.libroView;
  if (!instance) {
    return null;
  }
  var DndCellContainer = appInstance.dndContentRender;
  return /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellContainer, objectSpread2_default()({
    cell: observableCell,
    index: index
  }, props), cell.id);
});
var DndCellsRender = /*#__PURE__*/(0,react.forwardRef)(function DndCellsRender(_ref2, ref) {
  var libroView = _ref2.libroView,
    addCellButtons = _ref2.addCellButtons;
  var LoadingRender = (0,mana_observable_es/* getOrigin */.P$)(libroView.loadingRender);
  var cells = libroView.model.getCells().reduce(function (a, b) {
    if (a.indexOf(b) < 0) {
      a.push(b);
    }
    return a;
  }, []);
  var isInitialized = libroView.model.isInitialized;
  var isLoading = !isInitialized;
  var shouldRenderCells = isInitialized;
  return /*#__PURE__*/(0,jsx_runtime.jsx)(jsx_runtime.Fragment, {
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
      className: classnames_default()('libro-dnd-cells-container'),
      ref: ref,
      children: [isLoading && /*#__PURE__*/(0,jsx_runtime.jsx)(LoadingRender, {}), shouldRenderCells && /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        style: {
          height: '100%',
          overflow: 'visible'
        },
        children: cells.filter(function (cell) {
          return !cell.collapsedHidden;
        }).map(function (cell, index) {
          return /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellRender, {
            cell: cell,
            index: index
          }, cell.id);
        })
      })]
    })
  });
});
var LibroAppComponent = /*#__PURE__*/(0,react.memo)(function LibroAppComponent() {
  var ref = (0,react.useRef)(null);
  var libroViewTopRef = (0,react.useRef)(null);
  var libroViewRightContentRef = (0,react.useRef)(null);
  var libroViewLeftContentRef = (0,react.useRef)(null);
  var libroViewContentRef = (0,react.useRef)(null);
  var appInstance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var instance = appInstance.libroView;
  var handleScroll = (0,react.useCallback)(function () {
    var _instance$container, _instance$activeCell, _instance$activeCell2, _instance$activeCell3, _activeOutput$outputs, _instance$activeCell4, _libroViewTopRef$curr;
    if (!instance) {
      return;
    }
    instance.cellScrollEmitter.fire();
    var cellRightToolbar = (_instance$container = instance.container) === null || _instance$container === void 0 || (_instance$container = _instance$container.current) === null || _instance$container === void 0 ? void 0 : _instance$container.getElementsByClassName('libro-cell-right-toolbar')[instance.model.activeIndex];
    var activeCellOffsetY = (_instance$activeCell = instance.activeCell) === null || _instance$activeCell === void 0 || (_instance$activeCell = _instance$activeCell.container) === null || _instance$activeCell === void 0 || (_instance$activeCell = _instance$activeCell.current) === null || _instance$activeCell === void 0 ? void 0 : _instance$activeCell.getBoundingClientRect().y;
    var activeCellOffsetRight = (_instance$activeCell2 = instance.activeCell) === null || _instance$activeCell2 === void 0 || (_instance$activeCell2 = _instance$activeCell2.container) === null || _instance$activeCell2 === void 0 || (_instance$activeCell2 = _instance$activeCell2.current) === null || _instance$activeCell2 === void 0 ? void 0 : _instance$activeCell2.getBoundingClientRect().right;
    var activeOutput = libro_jupyter_es/* ExecutableCellView */.q0L.is(instance.activeCell) && ((_instance$activeCell3 = instance.activeCell) === null || _instance$activeCell3 === void 0 ? void 0 : _instance$activeCell3.outputArea);
    var activeOutputOffsetBottom = activeOutput && activeOutput.length > 0 ? activeOutput === null || activeOutput === void 0 || (_activeOutput$outputs = activeOutput.outputs[activeOutput.length - 1].container) === null || _activeOutput$outputs === void 0 || (_activeOutput$outputs = _activeOutput$outputs.current) === null || _activeOutput$outputs === void 0 ? void 0 : _activeOutput$outputs.getBoundingClientRect().bottom : (_instance$activeCell4 = instance.activeCell) === null || _instance$activeCell4 === void 0 || (_instance$activeCell4 = _instance$activeCell4.container) === null || _instance$activeCell4 === void 0 || (_instance$activeCell4 = _instance$activeCell4.current) === null || _instance$activeCell4 === void 0 ? void 0 : _instance$activeCell4.getBoundingClientRect().bottom;
    var libroViewTopOffsetBottom = (_libroViewTopRef$curr = libroViewTopRef.current) === null || _libroViewTopRef$curr === void 0 ? void 0 : _libroViewTopRef$curr.getBoundingClientRect().bottom;
    if (!cellRightToolbar) {
      return;
    }
    if (activeCellOffsetY !== undefined && libroViewTopOffsetBottom !== undefined && activeOutputOffsetBottom !== undefined && activeCellOffsetY <= libroViewTopOffsetBottom + 12 && activeOutputOffsetBottom >= libroViewTopOffsetBottom && activeCellOffsetRight !== undefined) {
      cellRightToolbar.style.cssText = "position:fixed;top:".concat(libroViewTopOffsetBottom + 12, "px;left:").concat(activeCellOffsetRight + 44 - 34, "px;right:unset;");
    } else {
      cellRightToolbar.style.cssText = '  position: absolute;top: 0px;right: -44px;';
    }
  }, [instance]);
  if (!instance) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-view-content",
    onScroll: handleScroll,
    ref: libroViewContentRef,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(es_button/* default */.ZP, {
      onClick: function onClick() {
        appInstance.serverConnection.makeRequest("".concat(appInstance.serverConnection.settings.baseUrl, "libro/api/ai/chatstream"), {
          method: 'POST',
          body: JSON.stringify({
            test: 'asd'
          })
        });
      }
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-view-content-left",
      ref: libroViewLeftContentRef,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        className: "libro-dnd-list-container",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellsRender, {
          libroView: instance,
          addCellButtons: null
        })
      })
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-view-content-right",
      ref: libroViewRightContentRef
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(back_top/* default */.Z, {
      target: function target() {
        return libroViewContentRef.current || document;
      },
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        className: "libro-totop-button",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(es_button/* default */.ZP, {
          shape: "circle",
          icon: /*#__PURE__*/(0,jsx_runtime.jsx)(ToTopOutlined/* default */.Z, {})
        })
      })
    })]
  });
});
var LibroAppView = (libro_app_view_dec = (0,mana_syringe_es/* transient */.H3)(), libro_app_view_dec2 = (0,decorator/* view */.ei)('libro-app'), libro_app_view_dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), libro_app_view_dec4 = (0,mana_observable_es/* prop */.vg)(), libro_app_view_dec5 = (0,mana_observable_es/* prop */.vg)(), libro_app_view_dec6 = (0,mana_observable_es/* prop */.vg)(), libro_app_view_dec7 = (0,mana_observable_es/* prop */.vg)(), _dec8 = (0,mana_observable_es/* prop */.vg)(), libro_app_view_dec(libro_app_view_class = libro_app_view_dec2(libro_app_view_class = (libro_app_view_class2 = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroAppView, _BaseView);
  var _super = createSuper_default()(LibroAppView);
  function LibroAppView(options, libroService) {
    var _this;
    classCallCheck_default()(this, LibroAppView);
    _this = _super.call(this);
    _this.libroService = void 0;
    _this.view = LibroAppComponent;
    _this.dndContentRender = AppCellContainer;
    _this.dndItemRender = DndCellItemRender;
    initializerDefineProperty_default()(_this, "serverConnection", libro_app_view_descriptor, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "libroView", libro_app_view_descriptor2, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "executeMessage", libro_app_view_descriptor3, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "executing", libro_app_view_descriptor4, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "executed", libro_app_view_descriptor5, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "succeed", libro_app_view_descriptor6, assertThisInitialized_default()(_this));
    _this.libroService = libroService;
    _this.libroService.getOrCreateView(options).then(function (view) {
      _this.libroView = view;
      _this.execute();
    });
    return _this;
  }
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* LibroService */.W$M)(LibroAppView, undefined, 1) || LibroAppView;
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(view_protocol/* ViewOption */.Hj)(LibroAppView, undefined, 0) || LibroAppView;
  createClass_default()(LibroAppView, [{
    key: "options",
    get: function get() {
      var _this$libroView;
      return (_this$libroView = this.libroView) === null || _this$libroView === void 0 ? void 0 : _this$libroView.model.options;
    }
  }, {
    key: "execute",
    value: function () {
      var _execute = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
        return regeneratorRuntime_default()().wrap(function _callee$(_context) {
          while (1) switch (_context.prev = _context.next) {
            case 0:
              if (this.libroView instanceof libro_jupyter_es/* LibroJupyterView */.lKf) {
                _context.next = 4;
                break;
              }
              this.executeMessage = '无法执行';
              this.succeed = false;
              return _context.abrupt("return");
            case 4:
              _context.prev = 4;
              this.executing = true;
              this.executeMessage = '准备 kernel...';
              _context.next = 9;
              return this.libroView.model.kcReady;
            case 9:
              this.executeMessage = '正在执行...';
              // TODO: use runCells result
              _context.next = 12;
              return this.libroView.runCells(this.libroView.model.cells);
            case 12:
              this.succeed = true;
              this.executing = false;
              _context.next = 19;
              break;
            case 16:
              _context.prev = 16;
              _context.t0 = _context["catch"](4);
              console.error(_context.t0);
            case 19:
            case "end":
              return _context.stop();
          }
        }, _callee, this, [[4, 16]]);
      }));
      function execute() {
        return _execute.apply(this, arguments);
      }
      return execute;
    }()
  }]);
  return LibroAppView;
}(default_view/* BaseView */.P), (libro_app_view_descriptor = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "serverConnection", [libro_app_view_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), libro_app_view_descriptor2 = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "libroView", [libro_app_view_dec4], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), libro_app_view_descriptor3 = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "executeMessage", [libro_app_view_dec5], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), libro_app_view_descriptor4 = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "executing", [libro_app_view_dec6], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return false;
  }
}), libro_app_view_descriptor5 = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "executed", [libro_app_view_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), libro_app_view_descriptor6 = applyDecoratedDescriptor_default()(libro_app_view_class2.prototype, "succeed", [_dec8], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return undefined;
  }
})), libro_app_view_class2)) || libro_app_view_class) || libro_app_view_class);
;// CONCATENATED MODULE: ./src/pages/interaction/execution-view.tsx










var execution_view_dec, execution_view_dec2, execution_view_dec3, execution_view_dec4, execution_view_dec5, execution_view_dec6, execution_view_dec7, execution_view_class, execution_view_class2, execution_view_descriptor, execution_view_descriptor2, execution_view_descriptor3, execution_view_descriptor4, execution_view_descriptor5;










function SubmitButton(props) {
  return /*#__PURE__*/_jsx(Button, {
    type: "primary",
    htmlType: "submit",
    children: "Submit"
  });
}
var LibroExecutionComponent = /*#__PURE__*/(0,react.forwardRef)(function (props, ref) {
  var formRef = (0,react.useRef)(null);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var queryParams = query_string/* default */.Z.parse(window.location.search);
  var filePath = queryParams['path'];
  var appView = (0,mana_observable_es/* useObserve */.Re)(instance.libroView);
  (0,react.useEffect)(function () {
    if (filePath && typeof filePath === 'string') {
      instance.path = filePath;
    }
  }, [filePath]);
  if (!queryParams['path']) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      children: "\u9700\u8981\u6307\u5B9A\u8981\u6267\u884C\u7684\u6587\u4EF6"
    });
  }
  if (!appView) {
    return null;
  }
  var handleSizeChange = function handleSizeChange(e) {
    instance.mode = e.target.value;
  };
  var children = null;
  if (instance.mode === 'notebook') {
    children = appView.libroView ? /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
      view: appView.libroView
    }) : null;
  } else {
    if (appView.executing) {
      children = /*#__PURE__*/(0,jsx_runtime.jsx)(spin/* default */.Z, {
        spinning: appView.executing,
        tip: "".concat(appView.executeMessage),
        children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
          style: {
            height: 200,
            width: '100%'
          }
        })
      });
    } else {
      if (appView.succeed) {
        children = /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
          view: appView
        });
      } else {
        children = /*#__PURE__*/(0,jsx_runtime.jsx)("span", {
          children: appView.executeMessage
        });
      }
    }
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-execution-container",
    ref: ref,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-execution-container-header",
      children: /*#__PURE__*/(0,jsx_runtime.jsxs)(es_radio/* default.Group */.ZP.Group, {
        value: instance.mode,
        onChange: handleSizeChange,
        children: [/*#__PURE__*/(0,jsx_runtime.jsx)(es_radio/* default.Button */.ZP.Button, {
          value: "app",
          children: "\u5E94\u7528\u9884\u89C8"
        }), /*#__PURE__*/(0,jsx_runtime.jsx)(es_radio/* default.Button */.ZP.Button, {
          value: "notebook",
          children: "notebook"
        })]
      })
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-execution-container-content",
      children: children
    })]
  });
});
var LibroExecutionView = (execution_view_dec = (0,mana_syringe_es/* singleton */.ri)(), execution_view_dec2 = (0,decorator/* view */.ei)('libro-execution-view'), execution_view_dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), execution_view_dec4 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* LibroFileService */.tL0), execution_view_dec5 = (0,mana_syringe_es/* inject */.f3)(view_manager/* ViewManager */.v), execution_view_dec6 = (0,mana_observable_es/* prop */.vg)(), execution_view_dec7 = (0,mana_observable_es/* prop */.vg)(), execution_view_dec(execution_view_class = execution_view_dec2(execution_view_class = (execution_view_class2 = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionView, _BaseView);
  var _super = createSuper_default()(LibroExecutionView);
  function LibroExecutionView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    initializerDefineProperty_default()(_this, "serverConnection", execution_view_descriptor, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "fileService", execution_view_descriptor2, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "viewManager", execution_view_descriptor3, assertThisInitialized_default()(_this));
    _this.view = LibroExecutionComponent;
    initializerDefineProperty_default()(_this, "libroView", execution_view_descriptor4, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "mode", execution_view_descriptor5, assertThisInitialized_default()(_this));
    _this._path = void 0;
    _this.update = /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
      return regeneratorRuntime_default()().wrap(function _callee$(_context) {
        while (1) switch (_context.prev = _context.next) {
          case 0:
            if (_this.path) {
              _context.next = 2;
              break;
            }
            return _context.abrupt("return");
          case 2:
            document.title = "interaction: ".concat(_this.path);
            _context.next = 5;
            return _this.viewManager.getOrCreateView(LibroAppView, {
              resource: _this.path
            });
          case 5:
            _this.libroView = _context.sent;
          case 6:
          case "end":
            return _context.stop();
        }
      }, _callee);
    }));
    return _this;
  }
  createClass_default()(LibroExecutionView, [{
    key: "path",
    get: function get() {
      return this._path;
    },
    set: function set(v) {
      this._path = v;
      this.update();
    }
  }]);
  return LibroExecutionView;
}(default_view/* BaseView */.P), (execution_view_descriptor = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "serverConnection", [execution_view_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor2 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "fileService", [execution_view_dec4], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor3 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "viewManager", [execution_view_dec5], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor4 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "libroView", [execution_view_dec6], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor5 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "mode", [execution_view_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return 'app';
  }
})), execution_view_class2)) || execution_view_class) || execution_view_class);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot.js
var slot = __webpack_require__(42681);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-react/es/index.js + 84 modules
var mana_react_es = __webpack_require__(25087);
;// CONCATENATED MODULE: ./src/pages/interaction/layout.tsx




var layout_dec, layout_dec2, layout_class;







var LibroExecutionLayoutSlots = {
  header: 'libro-execution-header',
  content: 'libro-execution-content'
};
var LibroExecutionLayoutComponent = /*#__PURE__*/(0,react.forwardRef)(function LibroExecutionLayoutComponent() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution-layout",
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)(mana_react_es/* BoxPanel */.jN, {
      direction: "top-to-bottom",
      children: [/*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-lab-layout-header",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(slot/* Slot */.g, {
          name: LibroExecutionLayoutSlots.header
        })
      }), /*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-lab-layout-container",
        flex: 1,
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(slot/* Slot */.g, {
          name: LibroExecutionLayoutSlots.content
        })
      })]
    })
  });
});
var LibroExecutionLayoutView = (layout_dec = (0,mana_syringe_es/* singleton */.ri)(), layout_dec2 = (0,decorator/* view */.ei)('libro-execution-layout'), layout_dec(layout_class = layout_dec2(layout_class = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionLayoutView, _BaseView);
  var _super = createSuper_default()(LibroExecutionLayoutView);
  function LibroExecutionLayoutView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionLayoutView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = LibroExecutionLayoutComponent;
    return _this;
  }
  return createClass_default()(LibroExecutionLayoutView);
}(default_view/* BaseView */.P)) || layout_class) || layout_class);
;// CONCATENATED MODULE: ./src/pages/interaction/execution-file.tsx








var execution_file_dec, execution_file_dec2, execution_file_dec3, execution_file_class, execution_file_class2, execution_file_descriptor;




var LibroExecutionFileComponent = /*#__PURE__*/(0,react.forwardRef)(function LibroExecutionFileComponent(props, ref) {
  var queryParams = query_string/* default */.Z.parse(window.location.search);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var filePath = queryParams['path'];
  (0,react.useEffect)(function () {
    if (filePath && typeof filePath === 'string') {
      instance.path = filePath;
    }
  }, [filePath]);
  if (!queryParams['path']) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution-file",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("h2", {
      children: instance.path
    })
  });
});
var LibroExecutionFileView = (execution_file_dec = (0,mana_syringe_es/* singleton */.ri)(), execution_file_dec2 = (0,decorator/* view */.ei)('libro-execution-file'), execution_file_dec3 = (0,mana_observable_es/* prop */.vg)(), execution_file_dec(execution_file_class = execution_file_dec2(execution_file_class = (execution_file_class2 = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionFileView, _BaseView);
  var _super = createSuper_default()(LibroExecutionFileView);
  function LibroExecutionFileView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionFileView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = LibroExecutionFileComponent;
    initializerDefineProperty_default()(_this, "_path", execution_file_descriptor, assertThisInitialized_default()(_this));
    return _this;
  }
  createClass_default()(LibroExecutionFileView, [{
    key: "path",
    get: function get() {
      return this._path;
    },
    set: function set(v) {
      this._path = v;
    }
  }]);
  return LibroExecutionFileView;
}(default_view/* BaseView */.P), (execution_file_descriptor = applyDecoratedDescriptor_default()(execution_file_class2.prototype, "_path", [execution_file_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), execution_file_class2)) || execution_file_class) || execution_file_class);
;// CONCATENATED MODULE: ./src/pages/interaction/index.tsx










var BaseModule = mana_module/* ManaModule */.R.create().register(LibroApp, LibroExecutionView, LibroExecutionLayoutView, LibroExecutionFileView, libro_lab_es/* BrandView */.S5B, LibroAppView, (0,decorator/* createSlotPreference */.vk)({
  slot: view_protocol/* RootSlotId */.lI,
  view: LibroExecutionLayoutView
}), (0,decorator/* createSlotPreference */.vk)({
  slot: LibroExecutionLayoutSlots.header,
  view: header_view/* HeaderView */.m
}), (0,decorator/* createSlotPreference */.vk)({
  slot: header_view/* HeaderArea */.M.middle,
  view: LibroExecutionFileView
}), (0,decorator/* createSlotPreference */.vk)({
  slot: header_view/* HeaderArea */.M.left,
  view: libro_lab_es/* BrandView */.S5B
}), (0,decorator/* createSlotPreference */.vk)({
  slot: LibroExecutionLayoutSlots.content,
  view: LibroExecutionView
}));
var LibroExecution = function LibroExecution() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(components/* ManaComponents */.rF.Application, {
      asChild: true,
      modules: [es/* ManaAppPreset */.n6L, libro_jupyter_es/* LibroJupyterModule */.MDs, libro_widget_es/* CommonWidgetsModule */.$B, BaseModule]
    }, "libro-execution")
  });
};
/* harmony default export */ var interaction = (LibroExecution);

/***/ }),

/***/ 80093:
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  Z: function() { return /* binding */ back_top; }
});

// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(67294);
// EXTERNAL MODULE: ./node_modules/@ant-design/icons/es/icons/VerticalAlignTopOutlined.js + 1 modules
var VerticalAlignTopOutlined = __webpack_require__(62635);
// EXTERNAL MODULE: ./node_modules/classnames/index.js
var classnames = __webpack_require__(93967);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);
// EXTERNAL MODULE: ./node_modules/rc-motion/es/index.js + 13 modules
var es = __webpack_require__(29372);
// EXTERNAL MODULE: ./node_modules/rc-util/es/omit.js
var omit = __webpack_require__(98423);
// EXTERNAL MODULE: ./node_modules/antd/es/_util/getScroll.js
var getScroll = __webpack_require__(66367);
// EXTERNAL MODULE: ./node_modules/antd/es/_util/reactNode.js
var reactNode = __webpack_require__(96159);
// EXTERNAL MODULE: ./node_modules/antd/es/_util/scrollTo.js + 1 modules
var scrollTo = __webpack_require__(58375);
// EXTERNAL MODULE: ./node_modules/antd/es/_util/throttleByAnimationFrame.js
var throttleByAnimationFrame = __webpack_require__(48783);
// EXTERNAL MODULE: ./node_modules/antd/es/config-provider/context.js
var context = __webpack_require__(53124);
// EXTERNAL MODULE: ./node_modules/@ant-design/cssinjs/es/index.js + 37 modules
var cssinjs_es = __webpack_require__(11568);
// EXTERNAL MODULE: ./node_modules/antd/es/style/index.js
var style = __webpack_require__(14747);
// EXTERNAL MODULE: ./node_modules/antd/es/theme/util/genStyleUtils.js
var genStyleUtils = __webpack_require__(83559);
// EXTERNAL MODULE: ./node_modules/@ant-design/cssinjs-utils/es/index.js + 12 modules
var cssinjs_utils_es = __webpack_require__(83262);
;// CONCATENATED MODULE: ./node_modules/antd/es/back-top/style/index.js



// ============================== Shared ==============================
const genSharedBackTopStyle = token => {
  const {
    componentCls,
    backTopFontSize,
    backTopSize,
    zIndexPopup
  } = token;
  return {
    [componentCls]: Object.assign(Object.assign({}, (0,style/* resetComponent */.Wf)(token)), {
      position: 'fixed',
      insetInlineEnd: token.backTopInlineEnd,
      insetBlockEnd: token.backTopBlockEnd,
      zIndex: zIndexPopup,
      width: 40,
      height: 40,
      cursor: 'pointer',
      '&:empty': {
        display: 'none'
      },
      [`${componentCls}-content`]: {
        width: backTopSize,
        height: backTopSize,
        overflow: 'hidden',
        color: token.backTopColor,
        textAlign: 'center',
        backgroundColor: token.backTopBackground,
        borderRadius: backTopSize,
        transition: `all ${token.motionDurationMid}`,
        '&:hover': {
          backgroundColor: token.backTopHoverBackground,
          transition: `all ${token.motionDurationMid}`
        }
      },
      // change to .backtop .backtop-icon
      [`${componentCls}-icon`]: {
        fontSize: backTopFontSize,
        lineHeight: (0,cssinjs_es/* unit */.bf)(backTopSize)
      }
    })
  };
};
const genMediaBackTopStyle = token => {
  const {
    componentCls,
    screenMD,
    screenXS,
    backTopInlineEndMD,
    backTopInlineEndXS
  } = token;
  return {
    [`@media (max-width: ${(0,cssinjs_es/* unit */.bf)(screenMD)})`]: {
      [componentCls]: {
        insetInlineEnd: backTopInlineEndMD
      }
    },
    [`@media (max-width: ${(0,cssinjs_es/* unit */.bf)(screenXS)})`]: {
      [componentCls]: {
        insetInlineEnd: backTopInlineEndXS
      }
    }
  };
};
const prepareComponentToken = token => ({
  zIndexPopup: token.zIndexBase + 10
});
// ============================== Export ==============================
/* harmony default export */ var back_top_style = ((0,genStyleUtils/* genStyleHooks */.I$)('BackTop', token => {
  const {
    fontSizeHeading3,
    colorTextDescription,
    colorTextLightSolid,
    colorText,
    controlHeightLG,
    calc
  } = token;
  const backTopToken = (0,cssinjs_utils_es/* mergeToken */.IX)(token, {
    backTopBackground: colorTextDescription,
    backTopColor: colorTextLightSolid,
    backTopHoverBackground: colorText,
    backTopFontSize: fontSizeHeading3,
    backTopSize: controlHeightLG,
    backTopBlockEnd: calc(controlHeightLG).mul(1.25).equal(),
    backTopInlineEnd: calc(controlHeightLG).mul(2.5).equal(),
    backTopInlineEndMD: calc(controlHeightLG).mul(1.5).equal(),
    backTopInlineEndXS: calc(controlHeightLG).mul(0.5).equal()
  });
  return [genSharedBackTopStyle(backTopToken), genMediaBackTopStyle(backTopToken)];
}, prepareComponentToken));
;// CONCATENATED MODULE: ./node_modules/antd/es/back-top/index.js
"use client";













const BackTop = props => {
  const {
    prefixCls: customizePrefixCls,
    className,
    rootClassName,
    visibilityHeight = 400,
    target,
    onClick,
    duration = 450
  } = props;
  const [visible, setVisible] = react.useState(visibilityHeight === 0);
  const ref = react.useRef(null);
  const getDefaultTarget = () => {
    var _a;
    return ((_a = ref.current) === null || _a === void 0 ? void 0 : _a.ownerDocument) || window;
  };
  const handleScroll = (0,throttleByAnimationFrame/* default */.Z)(e => {
    const scrollTop = (0,getScroll/* default */.Z)(e.target);
    setVisible(scrollTop >= visibilityHeight);
  });
  if (false) {}
  react.useEffect(() => {
    const getTarget = target || getDefaultTarget;
    const container = getTarget();
    handleScroll({
      target: container
    });
    container === null || container === void 0 ? void 0 : container.addEventListener('scroll', handleScroll);
    return () => {
      handleScroll.cancel();
      container === null || container === void 0 ? void 0 : container.removeEventListener('scroll', handleScroll);
    };
  }, [target]);
  const scrollToTop = e => {
    (0,scrollTo/* default */.Z)(0, {
      getContainer: target || getDefaultTarget,
      duration
    });
    onClick === null || onClick === void 0 ? void 0 : onClick(e);
  };
  const {
    getPrefixCls,
    direction
  } = react.useContext(context/* ConfigContext */.E_);
  const prefixCls = getPrefixCls('back-top', customizePrefixCls);
  const rootPrefixCls = getPrefixCls();
  const [wrapCSSVar, hashId, cssVarCls] = back_top_style(prefixCls);
  const classString = classnames_default()(hashId, cssVarCls, prefixCls, {
    [`${prefixCls}-rtl`]: direction === 'rtl'
  }, className, rootClassName);
  // fix https://fb.me/react-unknown-prop
  const divProps = (0,omit/* default */.Z)(props, ['prefixCls', 'className', 'rootClassName', 'children', 'visibilityHeight', 'target']);
  const defaultElement = /*#__PURE__*/react.createElement("div", {
    className: `${prefixCls}-content`
  }, /*#__PURE__*/react.createElement("div", {
    className: `${prefixCls}-icon`
  }, /*#__PURE__*/react.createElement(VerticalAlignTopOutlined/* default */.Z, null)));
  return wrapCSSVar(/*#__PURE__*/react.createElement("div", Object.assign({}, divProps, {
    className: classString,
    onClick: scrollToTop,
    ref: ref
  }), /*#__PURE__*/react.createElement(es/* default */.ZP, {
    visible: visible,
    motionName: `${rootPrefixCls}-fade`
  }, _ref => {
    let {
      className: motionClassName
    } = _ref;
    return (0,reactNode/* cloneElement */.Tm)(props.children || defaultElement, _ref2 => {
      let {
        className: cloneCls
      } = _ref2;
      return {
        className: classnames_default()(motionClassName, cloneCls)
      };
    });
  })));
};
if (false) {}
/* harmony default export */ var back_top = (BackTop);

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

/***/ }),

/***/ 13769:
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var objectWithoutPropertiesLoose = __webpack_require__(48541);
function _objectWithoutProperties(source, excluded) {
  if (source == null) return {};
  var target = objectWithoutPropertiesLoose(source, excluded);
  var key, i;
  if (Object.getOwnPropertySymbols) {
    var sourceSymbolKeys = Object.getOwnPropertySymbols(source);
    for (i = 0; i < sourceSymbolKeys.length; i++) {
      key = sourceSymbolKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
      target[key] = source[key];
    }
  }
  return target;
}
module.exports = _objectWithoutProperties, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 48541:
/***/ (function(module) {

function _objectWithoutPropertiesLoose(source, excluded) {
  if (source == null) return {};
  var target = {};
  var sourceKeys = Object.keys(source);
  var key, i;
  for (i = 0; i < sourceKeys.length; i++) {
    key = sourceKeys[i];
    if (excluded.indexOf(key) >= 0) continue;
    target[key] = source[key];
  }
  return target;
}
module.exports = _objectWithoutPropertiesLoose, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ })

}]);