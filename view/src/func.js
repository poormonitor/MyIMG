const logOut = () => {
    localStorage.removeItem("access_token_myimg");
    sessionStorage.removeItem("access_token_myimg");
};

const copyToClipboard = (text) => {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text);
    } else {
        var textarea = document.createElement("textarea");
        textarea.style.position = "fixed";
        textarea.style.clip = "rect(0 0 0 0)";
        textarea.style.top = "10px";
        textarea.value = text;
        textarea.select();
        document.execCommand("copy", true);
        document.body.removeChild(textarea);
    }
};

const decodeJWT = (token) => {
    if (!token) return {}

    const [header, payload, signature] = token.split('.');
    const decodedPayload = atob(payload);
    const jsonPayload = JSON.parse(decodedPayload);

    return jsonPayload;
}

export { logOut, copyToClipboard, decodeJWT };
