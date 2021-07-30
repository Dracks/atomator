import { EuiAccordion, EuiBadge, EuiTitle } from "@elastic/eui"
import React from "react"

import { GQLGqlApplication } from "../../../utils/graphql/generated"
import { getVerName } from "../versions/utils"
import BuildList from "./build-list"
import RepositoryRow from "./repository-row"
import TokenRow from "./token-row"

interface ApplicationDetailsProps {
    app: GQLGqlApplication
    reload: () => void
}

const ApplicationDetails: React.FC<ApplicationDetailsProps> = ({ app, reload }) => {
    return (
        <React.Fragment>
            <EuiTitle size="s" className="euiAccordionForm__title">
                <h3>{app.name}</h3>
            </EuiTitle>
            <EuiAccordion
                id="accordionForm1"
                className="euiAccordionForm"
                buttonClassName="euiAccordionForm__button"
                buttonContent="Tokens"
                extraAction={<EuiBadge>{app.tokenSet.length}</EuiBadge>}
                paddingSize="l"
            >
                {app.tokenSet.map(e => (
                    <TokenRow key={e.id} token={e} />
                ))}
            </EuiAccordion>
            <EuiAccordion
                id="accordionForm1"
                className="euiAccordionForm"
                buttonClassName="euiAccordionForm__button"
                buttonContent="Repositories"
                extraAction={<EuiBadge>{app.repositorySet.length}</EuiBadge>}
                paddingSize="l"
            >
                {app.repositorySet.map(r => (
                    <RepositoryRow key={r.id} repo={r} />
                ))}
            </EuiAccordion>
            <EuiAccordion
                id="accordionForm1"
                className="euiAccordionForm"
                buttonClassName="euiAccordionForm__button"
                buttonContent="Builds"
                extraAction={
                    <React.Fragment>
                        {app.lastRelease && (
                            <EuiBadge color="primary">
                                {getVerName(app.lastRelease)}
                            </EuiBadge>
                        )}
                        {app.lastBuild && (
                            <EuiBadge color="secondary">
                                {getVerName(app.lastBuild)}
                            </EuiBadge>
                        )}
                    </React.Fragment>
                }
                paddingSize="l"
            >
                <BuildList buildsList={app.buildSet} reload={reload} />
            </EuiAccordion>
        </React.Fragment>
    )
}

export default ApplicationDetails
