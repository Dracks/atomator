import React from "react"
import { CombinedError } from "urql"

import RestrictedContent from "./contents"
import { UserSessionContext } from "./contents/session/context"
import Login from "./contents/session/login"
import { useGetUserInfoQuery, useLogInMutation } from "./utils/graphql/generated"
import { LoadingPage } from "./utils/ui/loading"

interface SessionStatus {
    isLoading: boolean
    error?: CombinedError
    data?: {
        username: string
    }
}

const App: React.FC<{}> = () => {
    const [sessionQuery] = useGetUserInfoQuery()
    const [loginStatus, useLogin] = useLogInMutation()

    const [sessionStatus, setSession] = React.useState<SessionStatus>({
        isLoading: sessionQuery.fetching,
    })
    React.useEffect(() => {
        setSession({
            isLoading: sessionQuery.fetching,
            data: sessionQuery.data?.myProfile,
            error: sessionQuery.error,
        })
    }, [sessionQuery])

    const login = (username, password) => {
        useLogin({ username, password }).then(response => {
            setSession({
                ...sessionStatus,
                data: response.data?.session?.login?.profile,
            })
        })
    }
    if (sessionStatus.isLoading) {
        return <LoadingPage />
    } else {
        if (sessionStatus.data) {
            return (
                <UserSessionContext.Provider value={sessionStatus.data}>
                    <RestrictedContent />
                </UserSessionContext.Provider>
            )
        }
        return (
            <Login
                isLoading={loginStatus.fetching}
                login={login}
                error={loginStatus.data?.session?.login?.error}
            />
        )
    }
}

export default App
