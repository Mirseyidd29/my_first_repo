const API_URL = window.location.protocol === "file:"
  ? "http://localhost:8000/chat"
  : "/chat";
const MAX_HISTORY = 10;

let history = [];
let isOpen = false;

const chatPanel = document.getElementById("chat-panel");
const toggleBtn = document.getElementById("toggle-btn");
const btnAvatar = document.getElementById("btn-avatar");
const btnClose = document.getElementById("btn-close");
const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const emptyState = document.getElementById("empty-state");

toggleBtn.addEventListener("click", () => {
  isOpen = !isOpen;
  chatPanel.classList.toggle("open", isOpen);
  toggleBtn.classList.toggle("open", isOpen);
  btnAvatar.style.opacity = isOpen ? "0" : "1";
  btnClose.style.opacity = isOpen ? "1" : "0";
  if (isOpen) inputEl.focus();
});

function removeEmptyState() {
  if (emptyState) emptyState.remove();
}

function appendMessage(role, text) {
  removeEmptyState();

  const isUser = role === "user";
  const wrapper = document.createElement("div");
  wrapper.className = `flex items-end gap-2 ${isUser ? "justify-end" : "justify-start"}`;

  if (!isUser) {
    const avatar = document.createElement("img");
    avatar.src = "/static/atlas-avatar.png";
    avatar.className = "w-6 h-6 rounded-full object-cover flex-shrink-0 mb-0.5";
    wrapper.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = isUser
    ? "max-w-[78%] rounded-2xl rounded-br-sm px-3 py-2.5 text-white text-sm leading-relaxed"
    : "max-w-[78%] rounded-2xl rounded-bl-sm px-3 py-2.5 text-gray-100 text-sm leading-relaxed";
  bubble.style.background = isUser ? "#e41e26" : "#1e1e1e";
  bubble.textContent = text;

  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showTyping() {
  removeEmptyState();
  const wrapper = document.createElement("div");
  wrapper.id = "typing";
  wrapper.className = "flex items-end gap-2 justify-start";

  const avatar = document.createElement("img");
  avatar.src = "/static/atlas-avatar.png";
  avatar.className = "w-6 h-6 rounded-full object-cover flex-shrink-0 mb-0.5";
  wrapper.appendChild(avatar);

  const bubble = document.createElement("div");
  bubble.className = "rounded-2xl rounded-bl-sm px-3 py-2.5 text-zinc-500 text-sm";
  bubble.style.background = "#1e1e1e";
  bubble.textContent = "...";

  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typing");
  if (el) el.remove();
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  inputEl.value = "";
  sendBtn.disabled = true;

  appendMessage("user", text);
  showTyping();

  const payload = {
    message: text,
    history: history.slice(-MAX_HISTORY),
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    removeTyping();

    if (!res.ok) {
      appendMessage("assistant", `Server xətası (${res.status}). API key-i yoxla.`);
    } else {
      const data = await res.json();
      appendMessage("assistant", data.reply);

      history.push({ role: "user", content: text });
      history.push({ role: "assistant", content: data.reply });
      if (history.length > MAX_HISTORY) {
        history = history.slice(-MAX_HISTORY);
      }
    }
  } catch (err) {
    removeTyping();
    appendMessage("assistant", "Serverlə bağlantı yoxdur. uvicorn işləyirmi?");
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
