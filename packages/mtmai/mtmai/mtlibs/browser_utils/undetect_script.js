
console.log("设置额外的 反检测脚本");
//navigator.webdriver = false;
window.__pwInitScripts = undefined;
navigator.userAgentData = {
  "brands": [
    {
      "brand": "Google Chrome",
      "version": "135"
    },
    {
      "brand": "Not-A.Brand",
      "version": "8"
    },
    {
      "brand": "Chromium",
      "version": "135"
    }
  ],
  "mobile": false,
  "platform": "Windows"
}

Object.defineProperty(navigator, 'webdriver', {
  get: () => false,
});

// 禁用自动化标志
Object.defineProperty(navigator, 'permissions', {
  get: () => ({
    query: () => Promise.resolve({ state: 'granted' })
  })
});

// 修改时区
// Object.defineProperty(Intl, 'DateTimeFormat', {
//   get: () => {
//     return function () {
//       return {
//         resolvedOptions: () => ({
//           timeZone: 'Asia/Shanghai'
//         })
//       };
//     };
//   }
// });

// // 修改屏幕分辨率
// Object.defineProperty(window, 'screen', {
//   get: () => ({
//     width: 1920,
//     height: 1080,
//     colorDepth: 24,
//     pixelDepth: 24,
//   }),
// });

// // 修改 navigator 属性
// Object.defineProperty(navigator, 'platform', {
//   get: () => 'Win32',
// });

// 修改 canvas 指纹
const originalGetContext = HTMLCanvasElement.prototype.getContext;
HTMLCanvasElement.prototype.getContext = function (type) {
  const context = originalGetContext.apply(this, arguments);
  if (type === '2d') {
    const originalGetImageData = context.getImageData;
    context.getImageData = function () {
      const imageData = originalGetImageData.apply(this, arguments);
      // 添加一些随机噪声
      for (let i = 0; i < imageData.data.length; i += 4) {
        imageData.data[i] += Math.random() * 2 - 1;
      }
      return imageData;
    };
  }
  return context;
};


console.log("设置额外的 反检测脚本结束");