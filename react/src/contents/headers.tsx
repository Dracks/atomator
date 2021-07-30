import {
    EuiFlexGroup,
    EuiFlexItem,
    EuiHeader,
    EuiHeaderLink,
    EuiHeaderLinks,
    EuiHeaderLogo,
    EuiHeaderSection,
    EuiHeaderSectionItem,
    EuiLink,
    EuiText,
} from "@elastic/eui"
import React from "react"

import { getRouterLinkProps } from "../routing"
import useSessionContext from "./session/context"

const Headers: React.FC<{}> = () => {
    const defaultProps = React.useMemo(() => getRouterLinkProps("/"), [])
    const userInfo = useSessionContext()

    return (
        <EuiHeader>
            <EuiHeaderSectionItem border="right">
                <EuiHeaderLogo iconType="logoKibana" {...defaultProps}>
                    Atomator
                </EuiHeaderLogo>
            </EuiHeaderSectionItem>
            <EuiHeaderLinks>
                <EuiHeaderLink {...getRouterLinkProps("/applications")}>
                    Applications
                </EuiHeaderLink>
                <EuiHeaderLink {...getRouterLinkProps("/deploy")}>
                    Deploys
                </EuiHeaderLink>
            </EuiHeaderLinks>

            <EuiHeaderSection side="right">
                <EuiHeaderLinks>
                    <EuiFlexGroup>
                        <EuiFlexItem>
                            <EuiText>{userInfo.username}</EuiText>
                        </EuiFlexItem>
                        <EuiFlexItem grow={false}>
                            <EuiLink>Log out</EuiLink>
                        </EuiFlexItem>
                    </EuiFlexGroup>
                </EuiHeaderLinks>
            </EuiHeaderSection>
        </EuiHeader>
    )
}

export default Headers
