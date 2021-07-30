import { ApmRoute } from "@elastic/apm-rum-react"
import { EuiPage, EuiText } from "@elastic/eui"
import React from "react"
import { Route, Switch } from "react-router"

import HeaderContent from "../utils/version/version-name"
import ApplicationsIndex from "./applications"
import DeployIndex from "./deploy"
import MainPage from "./extra/main"
import NotFound from "./extra/not-found"
import Headers from "./headers"

const RestrictedContent: React.FC<{}> = () => (
    <React.Fragment>
        <Headers />
        <EuiPage>
            <Switch>
                <Route path="/" exact={true} component={MainPage} />
                <ApmRoute path="/applications" component={ApplicationsIndex} />
                <ApmRoute path="/deploy" component={DeployIndex} />
                <Route path="*" component={NotFound} />
            </Switch>
        </EuiPage>
        <EuiText size="xs" textAlign="center">
            Atomator (<HeaderContent name="version_name" />) by Jaume Singla Valls
            <br />
            Build <HeaderContent name="version_build" />
        </EuiText>
    </React.Fragment>
)

export default RestrictedContent
