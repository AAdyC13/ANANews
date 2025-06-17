document.addEventListener("DOMContentLoaded", function () {
    // 聊天相關元素
    const chatContainer = document.getElementById("chat_container");
    const textareaContent = document.getElementById("textarea_content");
    const btnSend = document.getElementById("btn_send");
    const btnClearMemory = document.getElementById("btn_clearMemory");
    const btnAiConnect = document.getElementById("btn_aiConnect");

    // 全域變數
    let token = null;
    let history = [];
    let isConnecting = false;

    // 創建聊天訊息元素
    function createMessageElement(content, isUser = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `d-flex mb-3 ${isUser ? 'justify-content-end' : 'justify-content-start'}`;

        const messageContentDiv = document.createElement("div");
        messageContentDiv.className = `px-3 py-2 rounded-3 ${isUser ? 'bg-primary text-light' : 'bg-light'}`;
        messageContentDiv.style.maxWidth = "80%";

        const textContent = document.createElement("div");
        textContent.innerHTML = content.replace(/\n/g, '<br>');

        messageContentDiv.appendChild(textContent);
        messageDiv.appendChild(messageContentDiv);
        return messageDiv;
    }

    // 添加訊息到聊天容器
    function addMessage(content, isUser = false) {
        const messageElement = createMessageElement(content, isUser);
        chatContainer.appendChild(messageElement);
        scrollToBottom();

        // 保存歷史紀錄
        history.push(content);
    }

    // 顯示系統訊息
    function showSystemMessage(content, isError = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `text-center my-2 ${isError ? 'text-danger' : 'text-muted'}`;
        messageDiv.innerHTML = `<small>${content}</small>`;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    // 確保滾動到底部的函數
    function scrollToBottom() {
        // 強制立即重新計算布局
        chatContainer.offsetHeight;
        // 滾動到底部
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 連接AI
    async function connectAI() {
        if (isConnecting) return;
        isConnecting = true;

        btnAiConnect.disabled = true;
        btnAiConnect.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 連線中...';

        try {
            const response = await fetch("api/ai_connection/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ password: textareaContent.value.trim() }),
            });

            const data = await response.json();

            if (response.ok && data.status === "success") {
                token = data.token;

                // 檢查是否需要清空聊天記錄（重新連線後的情況）
                if (btnAiConnect.getAttribute('data-need-reset') === 'true') {
                    showSystemMessage("🔄 根據系統要求，您的對話記錄已重置");
                    resetHistory();
                    btnAiConnect.removeAttribute('data-need-reset');
                } else {
                    showSystemMessage("🌊 成功連線！請開始提問吧！");
                }

                btnAiConnect.innerHTML = '<i class="bi bi-check-circle"></i> 已連線';
                btnAiConnect.className = "btn btn-success btn-sm";
                btnSend.disabled = false;
                btnClearMemory.disabled = false; // 啟用清除對話按鈕
            } else {
                showSystemMessage(`連線失敗: ${data.message}`, true);
                btnAiConnect.innerHTML = '<i class="bi bi-x-circle"></i> 連線失敗';
                btnAiConnect.className = "btn btn-danger btn-sm";
                // 移除對 resetHistory() 的調用，因為它是專門給達到對話上限的用戶使用的
                setTimeout(() => {
                    btnAiConnect.innerHTML = '<i class="bi bi-arrow-clockwise"></i> 重新連線';
                    btnAiConnect.className = "btn btn-warning btn-sm";
                    btnAiConnect.disabled = false;
                }, 3000);
            }
        } catch (error) {
            showSystemMessage(`連線錯誤: ${error.message}`, true);
            btnAiConnect.innerHTML = '<i class="bi bi-x-circle"></i> 連線錯誤';
            btnAiConnect.className = "btn btn-danger btn-sm";
            // 移除對 resetHistory() 的調用
            setTimeout(() => {
                btnAiConnect.innerHTML = '<i class="bi bi-arrow-clockwise"></i> 重新連線';
                btnAiConnect.className = "btn btn-warning btn-sm";
                btnAiConnect.disabled = false;
                btnSend.disabled = true;
            }, 3000);
        }

        isConnecting = false;
    }

    // 重置歷史記錄
    function resetHistory() {
        history = [];
        chatContainer.innerHTML = `
            <div class="text-center text-muted my-5">
                <p>🔄 系統已重置</p>
                <p>您的單次對話以達到上限，現在可以開始新的對話</p>
            </div>
        `;
    }

    // 發送訊息到AI
    async function sendMessage() {
        if (!token) {
            showSystemMessage("請先連線至AI", true);
            return;
        }

        const content = textareaContent.value.trim();
        if (!content) return;

        // 添加用戶訊息
        addMessage(content, true);
        textareaContent.value = "";

        // 顯示AI正在思考
        const thinkingDiv = document.createElement("div");
        thinkingDiv.className = "d-flex mb-3 justify-content-start";
        const thinkingContent = document.createElement("div");
        thinkingContent.className = "px-3 py-2 rounded-3 bg-light";
        thinkingContent.innerHTML = '<div class="typing-animation"><span>.</span><span>.</span><span>.</span></div>';
        thinkingDiv.appendChild(thinkingContent);
        chatContainer.appendChild(thinkingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // 禁用發送按鈕和清除對話按鈕
        btnSend.disabled = true;
        btnClearMemory.disabled = true; // 同時禁用清除對話按鈕

        // 創建 AbortController 用於超時中斷請求
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            controller.abort(); // 2分鐘後中斷請求
        }, 120000); // 120秒 = 2分鐘

        try {
            const response = await fetch("api/ai_talk/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({

                    sentence: content,
                    history: history
                }),
                signal: controller.signal // 添加 AbortController 的信號
            });

            // 清除超時計時器
            clearTimeout(timeoutId);

            const data = await response.json();

            // 移除思考動畫
            chatContainer.removeChild(thinkingDiv);

            if (response.ok && data.status === "success") {
                // 添加AI回覆
                addMessage(data.message);
                // 確保滾動到底部
                setTimeout(scrollToBottom, 100);
            } else {
                showSystemMessage(`AI回覆錯誤: ${data.message}`, true);

                if (data.message.includes("AUTO_RETRY")) {
                    token = null;
                    // 不立即清空記錄，但標記需要重置
                    showSystemMessage("您已達到單次對話上限。請點擊「重新連線」按鈕繼續對話，連線成功後系統將清空歷史記錄。", true);
                    showSystemMessage("您仍可繼續查看目前的對話內容，直到重新連線為止。", true);

                    btnAiConnect.innerHTML = '<i class="bi bi-arrow-clockwise"></i> 重新連線（將清空記錄）';
                    btnAiConnect.className = "btn btn-warning btn-sm";
                    btnAiConnect.disabled = false;
                    // 設置標記，表示下次連線成功後需要重置歷史
                    btnAiConnect.setAttribute('data-need-reset', 'true');

                    btnSend.disabled = true;
                    btnClearMemory.disabled = false; // 仍然可以手動清除對話

                    // 不再調用 resetHistory()，讓用戶可以查看對話紀錄
                }
            }
        } catch (error) {
            // 清除超時計時器
            clearTimeout(timeoutId);

            // 移除思考動畫
            chatContainer.removeChild(thinkingDiv);

            if (error.name === 'AbortError') {
                // 請求被中斷，顯示超時訊息
                showSystemMessage("回應時間過長，請稍後再試。AI 可能正在處理大量請求。", true);
            } else {
                // 其他錯誤
                showSystemMessage(`發送錯誤: ${error.message}`, true);
            }
        }

        // 重新啟用按鈕（除非是超過對話限制的情況，那麼在上面的程式碼中已經設置了按鈕狀態）
        if (!token) return; // 如果是因超過對話限制而導致token被清空，不執行以下啟用按鈕的操作
        btnSend.disabled = false;
        btnClearMemory.disabled = false; // 重新啟用清除對話按鈕
    }

    // 清除對話記錄
    function clearChat() {
        if (confirm("確定要清除所有對話記錄嗎？")) {
            history = [];
            chatContainer.innerHTML = `
                <div class="text-center text-muted my-5">
                    <p>👋 對話已清除</p>
                    <p>可以開始新的對話了</p>
                </div>
            `;
        }
    }

    // 按鈕事件綁定
    btnAiConnect.addEventListener("click", connectAI);
    btnClearMemory.addEventListener("click", clearChat);
    btnSend.addEventListener("click", sendMessage);

    // 按Enter發送訊息
    textareaContent.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // 初始化
    btnSend.disabled = true;  // 先禁用發送按鈕，直到連線成功
    btnClearMemory.disabled = true;  // 先禁用清除對話按鈕，直到連線成功

    // 添加CSS樣式
    const style = document.createElement("style");
    style.textContent = `
        #chat_container {
            scrollbar-width: thin;
            scrollbar-color: rgba(0,0,0,0.2) transparent;
        }
        #chat_container::-webkit-scrollbar {
            width: 6px;
        }
        #chat_container::-webkit-scrollbar-track {
            background: transparent;
        }
        #chat_container::-webkit-scrollbar-thumb {
            background-color: rgba(0,0,0,0.2);
            border-radius: 6px;
        }
        .typing-animation span {
            animation: typing 1.5s infinite;
            display: inline-block;
        }
        .typing-animation span:nth-child(2) {
            animation-delay: 0.5s;
        }
        .typing-animation span:nth-child(3) {
            animation-delay: 1s;
        }
        @keyframes typing {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});
