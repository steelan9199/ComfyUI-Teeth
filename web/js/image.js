import { app } from "../../../scripts/app.js";

// 确保这段代码在 DOM 加载完成后执行
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", addLink);
} else {
  addLink();
}
function addLink() {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.type = "text/css";
  // 使用相对路径引用 CSS 文件
  link.href = "/teeth/web/css/style.css";
  document.head.appendChild(link);
}
app.registerExtension({
  name: "comfy.teeth.imageWidgets",
  async nodeCreated(node) {
    // 开头做一个小隔离
    if (!node.comfyClass.startsWith("teeth ")) {
      return;
    }
    if (["teeth FindContours"].includes(node.comfyClass)) {
      const inputEl = document.createElement("textarea");
      inputEl.className = "comfy-multiline-input";
      inputEl.readOnly = true;
      inputEl.style.opacity = 0.6;
      const widget = node.addDOMWidget("info", "customtext", inputEl, {
        getValue() {
          return inputEl.value;
        },
        setValue(v) {
          inputEl.value = v;
        },
        serialize: false
      });
      widget.inputEl = inputEl;

      inputEl.addEventListener("input", () => {
        widget.callback?.(widget.value);
      });
    }
    if (["teeth RunPythonCode"].includes(node.comfyClass)) {
      const color = "#255073";
      node.bgcolor = color; // 设置背景颜色
      node.color = color; // 设置标题栏的颜色
    }
    if (["teeth SaveTextFile"].includes(node.comfyClass)) {
      const buttonEl = document.createElement("button");
      // buttonEl.className = "comfy-button"; // 你可以根据 ComfyUI 的样式修改类名
      buttonEl.textContent = "OpenDir"; // 设置按钮的文本
      buttonEl.type = "button"; // 指定按钮类型，避免在表单内默认的提交行为
      buttonEl.style.cursor = "pointer"; // 鼠标悬停时显示手型指针
      const widget = node.addDOMWidget("button", "OpenDir", buttonEl, {
        serialize: false
      });
      widget.buttonEl = buttonEl;
      buttonEl.addEventListener("click", () => {
        console.log("点击了按钮: OpenDir");
        //callback需要的参数,按你实际需求修改
        // widget.callback?.(buttonEl.value, LiteGraph.active_canvas, node, pos, event);
        // api方式获取路径
        const folder_Widget = node.widgets.find((w) => w.name === "folder");
        const data = {
          folder: folder_Widget.value,
        };
        fetch("/teeth/gemini/opendir", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        })
          .then((response) => response.json())
          .then((data) => {})
          .catch((error) => console.error("API请求失败:", error));
      });
      buttonEl.classList.add("teeth-open-dir-button");
    }
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (["teeth FindContours"].includes(nodeData.name)) {
      function populate(arr_text) {
        var text = "";
        for (let i = 0; i < arr_text.length; i++) {
          text += arr_text[i];
        }
        if (this.widgets) {
          const pos = this.widgets.findIndex((w) => w.name === "info");
          if (pos !== -1 && this.widgets[pos]) {
            const w = this.widgets[pos];
            w.value = text;
          }
        }
        requestAnimationFrame(() => {
          const sz = this.computeSize();
          if (sz[0] < this.size[0]) {
            sz[0] = this.size[0];
          }
          if (sz[1] < this.size[1]) {
            sz[1] = this.size[1];
          }
          this.onResize?.(sz);
          app.graph.setDirtyCanvas(true, false);
        });
      }

      // When the node is executed we will be sent the input text, display this in the widget
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        populate.call(this, message.text);
      };
    }
  }
});
