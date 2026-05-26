/**
 * copy-button.js — 为所有代码块添加一键复制按钮
 * 纯前端，零依赖，mkdocs 自动加载
 */
(function() {
  'use strict';

  function addCopyButtons() {
    document.querySelectorAll('pre code').forEach((codeBlock) => {
      // 避免重复添加
      if (codeBlock.closest('pre').querySelector('.copy-button')) return;

      const button = document.createElement('button');
      button.className = 'copy-button';
      button.textContent = '📋 复制';
      button.setAttribute('aria-label', '复制代码');

      Object.assign(button.style, {
        position: 'absolute',
        top: '8px',
        right: '8px',
        padding: '4px 10px',
        fontSize: '13px',
        border: '1px solid rgba(255,255,255,0.2)',
        borderRadius: '4px',
        background: 'rgba(0,0,0,0.5)',
        color: '#fff',
        cursor: 'pointer',
        zIndex: '10',
        transition: 'all 0.2s',
        opacity: '0',
      });

      const pre = codeBlock.closest('pre');
      pre.style.position = 'relative';
      pre.appendChild(button);

      // 鼠标进入显示按钮
      pre.addEventListener('mouseenter', () => { button.style.opacity = '1'; });
      pre.addEventListener('mouseleave', () => { button.style.opacity = '0'; });

      button.addEventListener('click', async () => {
        try {
          const text = codeBlock.textContent;
          await navigator.clipboard.writeText(text);
          button.textContent = '✅ 已复制';
          button.style.background = 'rgba(0,150,0,0.6)';
          setTimeout(() => {
            button.textContent = '📋 复制';
            button.style.background = 'rgba(0,0,0,0.5)';
          }, 2000);
        } catch (err) {
          button.textContent = '❌ 复制失败';
          setTimeout(() => { button.textContent = '📋 复制'; }, 2000);
        }
      });
    });
  }

  // 页面加载完成后执行，支持 mkdocs 的导航（页面切换时重新绑定）
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCopyButtons);
  } else {
    addCopyButtons();
  }

  // 监听 mkdocs 页面切换（material 主题使用 SPA 导航）
  document.addEventListener('DOMContentSwitch', addCopyButtons);
})();
