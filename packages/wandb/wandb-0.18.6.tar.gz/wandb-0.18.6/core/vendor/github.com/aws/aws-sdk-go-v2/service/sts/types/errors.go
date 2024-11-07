// Code generated by smithy-go-codegen DO NOT EDIT.

package types

import (
	"fmt"
	smithy "github.com/aws/smithy-go"
)

// The web identity token that was passed is expired or is not valid. Get a new
// identity token from the identity provider and then retry the request.
type ExpiredTokenException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *ExpiredTokenException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *ExpiredTokenException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *ExpiredTokenException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "ExpiredTokenException"
	}
	return *e.ErrorCodeOverride
}
func (e *ExpiredTokenException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// The request could not be fulfilled because the identity provider (IDP) that was
// asked to verify the incoming identity token could not be reached. This is often
// a transient error caused by network conditions. Retry the request a limited
// number of times so that you don't exceed the request rate. If the error
// persists, the identity provider might be down or not responding.
type IDPCommunicationErrorException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *IDPCommunicationErrorException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *IDPCommunicationErrorException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *IDPCommunicationErrorException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "IDPCommunicationError"
	}
	return *e.ErrorCodeOverride
}
func (e *IDPCommunicationErrorException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// The identity provider (IdP) reported that authentication failed. This might be
// because the claim is invalid.
//
// If this error is returned for the AssumeRoleWithWebIdentity operation, it can
// also mean that the claim has expired or has been explicitly revoked.
type IDPRejectedClaimException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *IDPRejectedClaimException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *IDPRejectedClaimException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *IDPRejectedClaimException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "IDPRejectedClaim"
	}
	return *e.ErrorCodeOverride
}
func (e *IDPRejectedClaimException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// The error returned if the message passed to DecodeAuthorizationMessage was
// invalid. This can happen if the token contains invalid characters, such as
// linebreaks.
type InvalidAuthorizationMessageException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *InvalidAuthorizationMessageException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *InvalidAuthorizationMessageException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *InvalidAuthorizationMessageException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "InvalidAuthorizationMessageException"
	}
	return *e.ErrorCodeOverride
}
func (e *InvalidAuthorizationMessageException) ErrorFault() smithy.ErrorFault {
	return smithy.FaultClient
}

// The web identity token that was passed could not be validated by Amazon Web
// Services. Get a new identity token from the identity provider and then retry the
// request.
type InvalidIdentityTokenException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *InvalidIdentityTokenException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *InvalidIdentityTokenException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *InvalidIdentityTokenException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "InvalidIdentityToken"
	}
	return *e.ErrorCodeOverride
}
func (e *InvalidIdentityTokenException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// The request was rejected because the policy document was malformed. The error
// message describes the specific error.
type MalformedPolicyDocumentException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *MalformedPolicyDocumentException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *MalformedPolicyDocumentException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *MalformedPolicyDocumentException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "MalformedPolicyDocument"
	}
	return *e.ErrorCodeOverride
}
func (e *MalformedPolicyDocumentException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// The request was rejected because the total packed size of the session policies
// and session tags combined was too large. An Amazon Web Services conversion
// compresses the session policy document, session policy ARNs, and session tags
// into a packed binary format that has a separate limit. The error message
// indicates by percentage how close the policies and tags are to the upper size
// limit. For more information, see [Passing Session Tags in STS]in the IAM User Guide.
//
// You could receive this error even though you meet other defined session policy
// and session tag limits. For more information, see [IAM and STS Entity Character Limits]in the IAM User Guide.
//
// [Passing Session Tags in STS]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html
// [IAM and STS Entity Character Limits]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-limits-entity-length
type PackedPolicyTooLargeException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *PackedPolicyTooLargeException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *PackedPolicyTooLargeException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *PackedPolicyTooLargeException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "PackedPolicyTooLarge"
	}
	return *e.ErrorCodeOverride
}
func (e *PackedPolicyTooLargeException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }

// STS is not activated in the requested region for the account that is being
// asked to generate credentials. The account administrator must use the IAM
// console to activate STS in that region. For more information, see [Activating and Deactivating Amazon Web Services STS in an Amazon Web Services Region]in the IAM
// User Guide.
//
// [Activating and Deactivating Amazon Web Services STS in an Amazon Web Services Region]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html
type RegionDisabledException struct {
	Message *string

	ErrorCodeOverride *string

	noSmithyDocumentSerde
}

func (e *RegionDisabledException) Error() string {
	return fmt.Sprintf("%s: %s", e.ErrorCode(), e.ErrorMessage())
}
func (e *RegionDisabledException) ErrorMessage() string {
	if e.Message == nil {
		return ""
	}
	return *e.Message
}
func (e *RegionDisabledException) ErrorCode() string {
	if e == nil || e.ErrorCodeOverride == nil {
		return "RegionDisabledException"
	}
	return *e.ErrorCodeOverride
}
func (e *RegionDisabledException) ErrorFault() smithy.ErrorFault { return smithy.FaultClient }
