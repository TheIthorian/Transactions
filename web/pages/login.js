import 'antd/dist/antd.css';
import { useState } from 'react';
import { useRouter } from 'next/router';
import { Button, Card, Col, Form, Input, Row } from 'antd';

import { Error } from 'components/error';
import { API_URL, API_KEY } from 'config';
import { makeStore } from 'util/store';
import { handleResponse } from 'util/rest';

// Consider putting this in a component. Then wrap in context
export default function Login() {
    const [error, setError] = useState(null);
    const store = makeStore('user');
    const router = useRouter();

    const login = async password => {
        const response = await fetch(API_URL + '/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Api-Key': API_KEY,
            },
            body: JSON.stringify({ password }),
        });

        const data = await handleResponse(response);

        if (data.logged_in) {
            store.set('session_id', data.session_id);
            router.push('/');
        } else {
            setError({ message: 'Incorrect password' });
        }
    };

    const onFinish = values => {
        setError(false);
        login(values.password).catch(err => {
            console.log(err);
            setError({ message: 'Error: Unable to log in.' });
        });
    };

    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
    };

    const renderError = () => {
        if (error) {
            return <Error error={error} />;
        }
        return <></>;
    };

    return (
        <div style={{ marginTop: 100 }}>
            <Row>
                <Col span={12} offset={6}>
                    <Card>
                        <h2>Login</h2>
                        <Form
                            name='login'
                            onFinish={onFinish}
                            onFinishFailed={onFinishFailed}
                            autoComplete='off'
                        >
                            {/* <Form.Item
                                label='Username'
                                name='username'
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input your username!',
                                    },
                                ]}
                            >
                                <Input />
                            </Form.Item> */}

                            <Form.Item
                                label='Password'
                                name='password'
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please provide a password',
                                    },
                                ]}
                            >
                                <Input.Password />
                            </Form.Item>

                            <Form.Item>
                                <Button type='primary' htmlType='submit'>
                                    Submit
                                </Button>
                            </Form.Item>
                            {renderError()}
                        </Form>
                    </Card>
                </Col>
            </Row>
        </div>
    );
}
