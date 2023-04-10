import {
    Button,
    Form,
    Input,
    Row,
    Col
} from 'antd';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const formItemLayout = {
    labelCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 8,
        },
    },
    wrapperCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 16,
        },
    },
};
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};
const Login = () => {
    const [form] = Form.useForm();
    const navigate = useNavigate();
    const [errors, setErrors] = useState([]);
    const onFinish = (values) => {
        console.log('Received values of form: ', values);
        const loginUser = async () => {
            try {
                const response = await axios.post(
                    "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/Login", values)
                if (response.data.statusCode === 200) {
                    setErrors(null)
                    console.log(response.data.jwt_token.AuthenticationResult.AccessToken)
                    localStorage.setItem('jwt_token', response.data.jwt_token.AuthenticationResult.AccessToken)
                    navigate('/dashboard')
                }
                if (response.data.statusCode === 400) {
                    setErrors(response.data.response)
                }
            } catch (e) {
                console.log(e)
                console.log(e.response.status)
            }
        };
        loginUser();
    };

    return (
        <Row type="flex" justify="center" align="middle" style={{ minHeight: '100vh' }}>
            <Col>
                <div>
                    <h2> Log in </h2>
                    {console.log(errors)}
                    {errors && <h2>{errors}</h2>}
                    <Form
                        {...formItemLayout}
                        form={form}
                        name="register"
                        onFinish={onFinish}
                        initialValues={{
                            prefix: '+1',
                        }}
                        style={{
                            maxWidth: 600,
                        }}
                        scrollToFirstError
                    >

                        <Form.Item
                            name="email"
                            label="E-mail"
                            rules={[
                                {
                                    type: 'email',
                                    message: 'The input is not valid E-mail!',
                                },
                                {
                                    required: true,
                                    message: 'Please input your E-mail!',
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>

                        <Form.Item
                            name="password"
                            label="Password"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please input your password!',
                                },
                            ]}
                            hasFeedback
                        >
                            <Input.Password />
                        </Form.Item>

                        <Form.Item {...tailFormItemLayout}>
                            <Button type="primary" htmlType="submit">
                                Login
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            </Col>
        </Row>
    );
};
export default Login;