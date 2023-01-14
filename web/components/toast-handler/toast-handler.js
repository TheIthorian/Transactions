import { Alert } from 'antd';
import { useEffect, useState } from 'react';

import { ALTERT_DURATION } from './constants';
import styles from './toast-handler.module.css';

export function ToastHandler() {
    const [toast, setToast] = useState({
        title: null,
        message: null,
        type: null,
    });
    const [display, setDisplay] = useState(false);
    let toastTimeout;

    const handleDisplayToast = event => {
        const { title, message, type } = event.detail;
        setToast({ title, message, type });
        clearTimeout(toastTimeout);
        setDisplay(true);
        toastTimeout = setTimeout(() => setDisplay(false), ALTERT_DURATION);
    };

    useEffect(() => {
        window.addEventListener('toast', handleDisplayToast);
    });

    return (
        <div className={styles.container}>
            <div className={styles['toast-handler']}>{display && <Toast toast={toast} />}</div>
        </div>
    );
}

function Toast({ toast }) {
    const { title, message, type } = toast;
    if (title) {
        return <Alert {...{ title, message, type }} showIcon closable />;
    } else {
        return <Alert {...{ message, type }} showIcon closable />;
    }
}
