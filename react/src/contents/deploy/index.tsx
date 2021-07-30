import React from "react"
import { Route, Switch } from "react-router"

import DeployDetails from "./details"
import DeployList from "./list"
import DeployWizard from "./wizard"

const DeployIndex: React.FC<{}> = () => (
    <React.Fragment>
        <Switch>
            <Route path="/deploy" exact={true} component={DeployList} />
            <Route path="/deploy/new/:buildId" component={DeployWizard} />
            <Route path="/deploy/:deployId" component={DeployDetails} />
        </Switch>
    </React.Fragment>
)

export default DeployIndex
