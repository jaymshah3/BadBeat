export function isInvalidNum(data) {
    return isNaN(data) || data == '' || parseInt(data) < 0;
}

export function isUnsanitized(data) {
    return data == "";
}