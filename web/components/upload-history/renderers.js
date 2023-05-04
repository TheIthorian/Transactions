import { LABELS } from 'components/i18n';

const STATUS_MAP = {
    COMPLETE: LABELS.uploadStatuses.complete,
    PENDING: LABELS.uploadStatuses.pending,
    ERROR: LABELS.uploadStatuses.error,
};

export function makeFilenameRenderer() {
    return (_, record) => {
        const { file_name } = record;
        const MAX_LENGTH = 50;
        if (file_name.length > MAX_LENGTH) {
            return file_name.substring(0, MAX_LENGTH) + '...';
        }

        return file_name;
    };
}

export function makeSizeRenderer() {
    return (_, record) => {
        const { size } = record;
        const sizeInKb = Math.max(size / 1000, 1);
        return Number(sizeInKb.toFixed(0)).toLocaleString() + ' kb';
    };
}

export function makeDateRenderer() {
    return text => {
        if (text) {
            const date = new Date(text);
            return date?.toLocaleString('en-GB', {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
            });
        }
    };
}

export function makeStatusRenderer() {
    return (_, record) => {
        const { status } = record;
        return STATUS_MAP[status] ?? LABELS.uploadUnknownStatus;
    };
}
