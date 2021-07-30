import React from "react"

interface UserSession {
    username?: string
}

export const UserSessionContext = React.createContext<UserSession>({})

const useSessionContext = () => React.useContext(UserSessionContext)

export default useSessionContext
