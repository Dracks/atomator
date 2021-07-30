import React from "react"
import { withRouter } from "react-router"
import { BrowserRouter as Router } from "react-router-dom"
import { Provider as UrqlProvider } from "urql"

import { registerRouter } from "../../routing"
import graphQLClient from "../graphql/client"

const RegisterRouter = withRouter(({ history, children }: any) => {
    React.useEffect(() => {
        const router = {
            history,
        }
        registerRouter(router)
    })
    return children
})

const AllProviders: React.FC<{}> = ({ children }) => {
    return (
        <UrqlProvider value={graphQLClient()}>
            <Router basename="/ui">
                <RegisterRouter>{children}</RegisterRouter>
            </Router>
        </UrqlProvider>
    )
}

export default AllProviders
