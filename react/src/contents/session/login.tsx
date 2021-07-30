import {
    EuiButton,
    EuiFieldText,
    EuiForm,
    EuiFormProps,
    EuiFormRow,
    EuiPage,
    EuiPageBody,
    EuiPageContent,
    EuiPageContentBody,
    EuiPageContentHeader,
    EuiPageContentHeaderSection,
    EuiTitle,
} from "@elastic/eui"
import React from "react"

import { ErrorsCode } from "../../utils/errors"

interface LoginProps {
    login: (username: string, password: string) => void
    isLoading: boolean
    error?: { code: number }
}

const ERRORS_TEXT: { [key in ErrorsCode]?: string } = {
    [ErrorsCode.userNotFound]: "Credentials not valid",
}

const Login = ({ login, isLoading, error }: LoginProps) => {
    const [username, setUsername] = React.useState("")
    const [password, setPassword] = React.useState("")
    let formProps: EuiFormProps = {}
    if (error) {
        formProps = {
            isInvalid: true,
            error: ERRORS_TEXT[error.code],
        }
    }
    return (
        <EuiPage>
            <EuiPageBody>
                <EuiPageContent verticalPosition="center" horizontalPosition="center">
                    <EuiPageContentHeader>
                        <EuiPageContentHeaderSection>
                            <EuiTitle>
                                <h2>Login</h2>
                            </EuiTitle>
                        </EuiPageContentHeaderSection>
                    </EuiPageContentHeader>
                    <EuiPageContentBody>
                        <EuiForm {...formProps}>
                            <EuiFormRow label="Username">
                                <EuiFieldText
                                    name="username"
                                    value={username}
                                    onChange={(event: any) =>
                                        setUsername(event.target.value)
                                    }
                                />
                            </EuiFormRow>

                            <EuiFormRow label="Password">
                                <EuiFieldText
                                    type="Password"
                                    value={password}
                                    onChange={(event: any) =>
                                        setPassword(event.target.value)
                                    }
                                />
                            </EuiFormRow>

                            <EuiButton
                                fill
                                isLoading={isLoading}
                                onClick={() => login(username, password)}
                            >
                                Login
                            </EuiButton>
                        </EuiForm>
                    </EuiPageContentBody>
                </EuiPageContent>
            </EuiPageBody>
        </EuiPage>
    )
}

export default Login
