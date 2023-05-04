import { useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';

import { Error } from 'components/error';
import { UploadHistory } from 'components/upload-history';

import { addUpload } from './data';
import { LABELS } from '../i18n';

const { Dragger } = Upload;

export default function TransactionUpload() {
    const [error, setError] = useState(null);

    function setSafeError(error) {
        error.safe = true;
        setError(error);
    }

    function handleUpload(value) {
        if (!value) return;

        const newItem = { l1: value, amount: 0 };
        addUpload().catch(setSafeError);
    }

    if (error && !error.safe) {
        return <Error error={error} />;
    }

    const props = {
        name: 'file',
        multiple: true,
        action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
        onChange(info) {
            const { status } = info.file;
            if (status !== 'uploading') {
                console.log(info.file, info.fileList);
            }
            if (status === 'done') {
                message.success(`${info.file.name} file uploaded successfully.`);
            } else if (status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        },
        onDrop(e) {
            console.log('Dropped files', e.dataTransfer.files);
        },
    };

    return (
        <div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <h1>{LABELS.uploadPageTitle}</h1>
            </div>
            <Dragger {...props}>
                <p className='ant-upload-drag-icon'>
                    <InboxOutlined />
                </p>
                <p className='ant-upload-text'>{LABELS.uploadDragAreaTitle}</p>
                <p className='ant-upload-hint'>{LABELS.uploadDragAreaSubtitle}</p>
            </Dragger>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <UploadHistory />
            </div>
        </div>
    );
}
