import {
    EuiPageContent,
    EuiPageContentBody,
    EuiPageContentHeader,
    EuiPageContentHeaderSection,
    EuiTitle,
} from "@elastic/eui"
import React from "react"

const NotFound = () => (
    <EuiPageContent>
        <EuiPageContentHeader>
            <EuiPageContentHeaderSection>
                <EuiTitle>
                    <h2>Not found</h2>
                </EuiTitle>
            </EuiPageContentHeaderSection>
        </EuiPageContentHeader>
        <EuiPageContentBody>404 Content not found</EuiPageContentBody>
    </EuiPageContent>
)

export default NotFound
