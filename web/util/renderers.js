export function makeDateRenderer() {
    return text => {
        if (text) {
            const date = new Date(text);
            return date?.toLocaleString('en-GB', { timeZone: 'UTC' });
        }
    };
}
