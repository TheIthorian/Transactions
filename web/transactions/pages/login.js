import { useState } from 'react';
import { useRouter } from 'next/router';
import { Button, Card, Col, Form, Input, Row } from 'antd';

import { Error } from 'components/error';
import { API_URL, API_KEY } from 'config';
import { makeStore } from 'util/store';

// Consider putting this in a component. Then wrap in context
export default function Login() {
    const [error, setError] = useState(false);
    const store = makeStore('user');
    const router = useRouter();

    const login = async password => {
        let response = await fetch(API_URL + '/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Api-Key': API_KEY,
            },
            body: JSON.stringify({ password }),
        });
        response = await response.json();
        store.set('password', password);
        router.push('/');
    };

    const onFinish = values => {
        setError(false);
        login(values.password).catch(err => {
            console.log(err);
            setError(true);
        });
    };

    const onFinishFailed = errorInfo => {
        console.log('Failed:', errorInfo);
    };

    const renderError = () => {
        if (error) {
            const display = { message: 'Error: Unable to log in.' };
            return <Error error={display} />;
        }
        return <></>;
    };

    return (
        <>
            <h1>Login</h1>
            <Row>
                <Col span={12} offset={6}>
                    <Card>
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
        </>
    );
}
