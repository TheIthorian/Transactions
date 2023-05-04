import { useState } from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { Button, Form, message, Space, Upload } from 'antd';

import { Error } from 'components/error';
import { UploadHistory } from 'components/upload-history';
import { makeStore } from 'util/store';
import { API_URL, API_KEY } from 'config';

import { addUpload } from './data';
import { LABELS } from '../i18n';

const { Dragger } = Upload;

export default function TransactionUpload() {
    const [files, setFiles] = useState(null);

    async function handleFinish(e) {
        const formData = new FormData();
        formData.append('file', files);
        await addUpload(formData).catch(error =>
            message.error(`Unable to upload file: ${error.title}`)
        );
    }

    function handleFinishFailed(e) {
        console.error(e);
    }

    function handleFinishDrag(info) {
        const { status, originFileObj } = info.file;
        if (status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (status === 'done') {
            message.success(`${info.file.name} file uploaded successfully.`);
        } else if (status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }

        setFiles(originFileObj);
    }

    function handleDrop(e) {
        console.log('Dropped files', e.dataTransfer.files);
    }

    return (
        <div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <h1>{LABELS.uploadPageTitle}</h1>
            </div>
            <Form
                name='file-upload'
                onFinish={handleFinish}
                onFinishFailed={handleFinishFailed}
                autoComplete='off'
            >
                <Form.Item name='newFiles'>
                    <div
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'center',
                            alignItems: 'center',
                        }}
                    >
                        <div
                            style={{
                                width: '100%',
                                maxWidth: 1200,
                            }}
                        >
                            <Dragger
                                {...{
                                    name: 'draggerElementFile',
                                    multiple: true,
                                    accept: '.csv,.txt',
                                    onChange: info => handleFinishDrag(info),
                                    onDrop: handleDrop,
                                }}
                                style={{ padding: 30 }}
                            >
                                <p className='ant-upload-drag-icon'>
                                    <InboxOutlined />
                                </p>
                                <p className='ant-upload-text'>{LABELS.uploadDragAreaTitle}</p>
                                <p className='ant-upload-hint'>{LABELS.uploadDragAreaSubtitle}</p>
                            </Dragger>
                        </div>
                    </div>
                </Form.Item>
                <Form.Item>
                    <Button type='primary' htmlType='submit' disabled={!files}>
                        {LABELS.submit}
                    </Button>
                </Form.Item>
            </Form>
            <span>{files?.name}</span>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <UploadHistory />
            </div>
        </div>
    );
}
