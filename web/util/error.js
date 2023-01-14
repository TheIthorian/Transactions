class CustomError extends Error {
    title;
    message = '';

    constructor({ title, message, detail }) {
        super(message);
        this.title = title;
        this.message = message ?? detail.Error;
        this.detail = detail;
        console.log('Error: ', { title, message, detail });
    }
}

export function makeCustomError({ title, message, detail }) {
    return new CustomError({ title, message, detail });
}

export function dispatchErrorToast(error) {
    const toastEvent = new Event('toast');
    toastEvent.detail = {
        message: error.message,
        type: 'error',
    };
    window.dispatchEvent(toastEvent);
}
