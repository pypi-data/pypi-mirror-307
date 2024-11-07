// Code generated by smithy-go-codegen DO NOT EDIT.

package s3

import (
	"context"
	"fmt"
	awsmiddleware "github.com/aws/aws-sdk-go-v2/aws/middleware"
	"github.com/aws/aws-sdk-go-v2/aws/signer/v4"
	s3cust "github.com/aws/aws-sdk-go-v2/service/s3/internal/customizations"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
	"github.com/aws/smithy-go/middleware"
	smithyhttp "github.com/aws/smithy-go/transport/http"
)

// This operation lists in-progress multipart uploads in a bucket. An in-progress
// multipart upload is a multipart upload that has been initiated by the
// CreateMultipartUpload request, but has not yet been completed or aborted.
//
// Directory buckets - If multipart uploads in a directory bucket are in progress,
// you can't delete the bucket until all the in-progress multipart uploads are
// aborted or completed. To delete these in-progress multipart uploads, use the
// ListMultipartUploads operation to list the in-progress multipart uploads in the
// bucket and use the AbortMultupartUpload operation to abort all the in-progress
// multipart uploads.
//
// The ListMultipartUploads operation returns a maximum of 1,000 multipart uploads
// in the response. The limit of 1,000 multipart uploads is also the default value.
// You can further limit the number of uploads in a response by specifying the
// max-uploads request parameter. If there are more than 1,000 multipart uploads
// that satisfy your ListMultipartUploads request, the response returns an
// IsTruncated element with the value of true , a NextKeyMarker element, and a
// NextUploadIdMarker element. To list the remaining multipart uploads, you need to
// make subsequent ListMultipartUploads requests. In these requests, include two
// query parameters: key-marker and upload-id-marker . Set the value of key-marker
// to the NextKeyMarker value from the previous response. Similarly, set the value
// of upload-id-marker to the NextUploadIdMarker value from the previous response.
//
// Directory buckets - The upload-id-marker element and the NextUploadIdMarker
// element aren't supported by directory buckets. To list the additional multipart
// uploads, you only need to set the value of key-marker to the NextKeyMarker
// value from the previous response.
//
// For more information about multipart uploads, see [Uploading Objects Using Multipart Upload] in the Amazon S3 User Guide.
//
// Directory buckets - For directory buckets, you must make requests for this API
// operation to the Zonal endpoint. These endpoints support virtual-hosted-style
// requests in the format
// https://bucket_name.s3express-az_id.region.amazonaws.com/key-name . Path-style
// requests are not supported. For more information, see [Regional and Zonal endpoints]in the Amazon S3 User
// Guide.
//
// Permissions
//
//   - General purpose bucket permissions - For information about permissions
//     required to use the multipart upload API, see [Multipart Upload and Permissions]in the Amazon S3 User Guide.
//
//   - Directory bucket permissions - To grant access to this API operation on a
//     directory bucket, we recommend that you use the [CreateSession]CreateSession API operation
//     for session-based authorization. Specifically, you grant the
//     s3express:CreateSession permission to the directory bucket in a bucket policy
//     or an IAM identity-based policy. Then, you make the CreateSession API call on
//     the bucket to obtain a session token. With the session token in your request
//     header, you can make API requests to this operation. After the session token
//     expires, you make another CreateSession API call to generate a new session
//     token for use. Amazon Web Services CLI or SDKs create session and refresh the
//     session token automatically to avoid service interruptions when a session
//     expires. For more information about authorization, see [CreateSession]CreateSession .
//
// Sorting of multipart uploads in response
//
//   - General purpose bucket - In the ListMultipartUploads response, the multipart
//     uploads are sorted based on two criteria:
//
//   - Key-based sorting - Multipart uploads are initially sorted in ascending
//     order based on their object keys.
//
//   - Time-based sorting - For uploads that share the same object key, they are
//     further sorted in ascending order based on the upload initiation time. Among
//     uploads with the same key, the one that was initiated first will appear before
//     the ones that were initiated later.
//
//   - Directory bucket - In the ListMultipartUploads response, the multipart
//     uploads aren't sorted lexicographically based on the object keys.
//
// HTTP Host header syntax  Directory buckets - The HTTP Host header syntax is
// Bucket_name.s3express-az_id.region.amazonaws.com .
//
// The following operations are related to ListMultipartUploads :
//
// [CreateMultipartUpload]
//
// [UploadPart]
//
// [CompleteMultipartUpload]
//
// [ListParts]
//
// [AbortMultipartUpload]
//
// [Uploading Objects Using Multipart Upload]: https://docs.aws.amazon.com/AmazonS3/latest/dev/uploadobjusingmpu.html
// [ListParts]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html
// [AbortMultipartUpload]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_AbortMultipartUpload.html
// [UploadPart]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html
// [Regional and Zonal endpoints]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-Regions-and-Zones.html
// [CreateSession]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateSession.html
// [Multipart Upload and Permissions]: https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuAndPermissions.html
// [CompleteMultipartUpload]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html
// [CreateMultipartUpload]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateMultipartUpload.html
func (c *Client) ListMultipartUploads(ctx context.Context, params *ListMultipartUploadsInput, optFns ...func(*Options)) (*ListMultipartUploadsOutput, error) {
	if params == nil {
		params = &ListMultipartUploadsInput{}
	}

	result, metadata, err := c.invokeOperation(ctx, "ListMultipartUploads", params, optFns, c.addOperationListMultipartUploadsMiddlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*ListMultipartUploadsOutput)
	out.ResultMetadata = metadata
	return out, nil
}

type ListMultipartUploadsInput struct {

	// The name of the bucket to which the multipart upload was initiated.
	//
	// Directory buckets - When you use this operation with a directory bucket, you
	// must use virtual-hosted-style requests in the format
	// Bucket_name.s3express-az_id.region.amazonaws.com . Path-style requests are not
	// supported. Directory bucket names must be unique in the chosen Availability
	// Zone. Bucket names must follow the format bucket_base_name--az-id--x-s3 (for
	// example, DOC-EXAMPLE-BUCKET--usw2-az1--x-s3 ). For information about bucket
	// naming restrictions, see [Directory bucket naming rules]in the Amazon S3 User Guide.
	//
	// Access points - When you use this action with an access point, you must provide
	// the alias of the access point in place of the bucket name or specify the access
	// point ARN. When using the access point ARN, you must direct requests to the
	// access point hostname. The access point hostname takes the form
	// AccessPointName-AccountId.s3-accesspoint.Region.amazonaws.com. When using this
	// action with an access point through the Amazon Web Services SDKs, you provide
	// the access point ARN in place of the bucket name. For more information about
	// access point ARNs, see [Using access points]in the Amazon S3 User Guide.
	//
	// Access points and Object Lambda access points are not supported by directory
	// buckets.
	//
	// S3 on Outposts - When you use this action with Amazon S3 on Outposts, you must
	// direct requests to the S3 on Outposts hostname. The S3 on Outposts hostname
	// takes the form
	// AccessPointName-AccountId.outpostID.s3-outposts.Region.amazonaws.com . When you
	// use this action with S3 on Outposts through the Amazon Web Services SDKs, you
	// provide the Outposts access point ARN in place of the bucket name. For more
	// information about S3 on Outposts ARNs, see [What is S3 on Outposts?]in the Amazon S3 User Guide.
	//
	// [Directory bucket naming rules]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-naming-rules.html
	// [What is S3 on Outposts?]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html
	// [Using access points]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-access-points.html
	//
	// This member is required.
	Bucket *string

	// Character you use to group keys.
	//
	// All keys that contain the same string between the prefix, if specified, and the
	// first occurrence of the delimiter after the prefix are grouped under a single
	// result element, CommonPrefixes . If you don't specify the prefix parameter, then
	// the substring starts at the beginning of the key. The keys that are grouped
	// under CommonPrefixes result element are not returned elsewhere in the response.
	//
	// Directory buckets - For directory buckets, / is the only supported delimiter.
	Delimiter *string

	// Encoding type used by Amazon S3 to encode the [object keys] in the response. Responses are
	// encoded only in UTF-8. An object key can contain any Unicode character. However,
	// the XML 1.0 parser can't parse certain characters, such as characters with an
	// ASCII value from 0 to 10. For characters that aren't supported in XML 1.0, you
	// can add this parameter to request that Amazon S3 encode the keys in the
	// response. For more information about characters to avoid in object key names,
	// see [Object key naming guidelines].
	//
	// When using the URL encoding type, non-ASCII characters that are used in an
	// object's key name will be percent-encoded according to UTF-8 code values. For
	// example, the object test_file(3).png will appear as test_file%283%29.png .
	//
	// [Object key naming guidelines]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-guidelines
	// [object keys]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
	EncodingType types.EncodingType

	// The account ID of the expected bucket owner. If the account ID that you provide
	// does not match the actual owner of the bucket, the request fails with the HTTP
	// status code 403 Forbidden (access denied).
	ExpectedBucketOwner *string

	// Specifies the multipart upload after which listing should begin.
	//
	//   - General purpose buckets - For general purpose buckets, key-marker is an
	//   object key. Together with upload-id-marker , this parameter specifies the
	//   multipart upload after which listing should begin.
	//
	// If upload-id-marker is not specified, only the keys lexicographically greater
	//   than the specified key-marker will be included in the list.
	//
	// If upload-id-marker is specified, any multipart uploads for a key equal to the
	//   key-marker might also be included, provided those multipart uploads have
	//   upload IDs lexicographically greater than the specified upload-id-marker .
	//
	//   - Directory buckets - For directory buckets, key-marker is obfuscated and
	//   isn't a real object key. The upload-id-marker parameter isn't supported by
	//   directory buckets. To list the additional multipart uploads, you only need to
	//   set the value of key-marker to the NextKeyMarker value from the previous
	//   response.
	//
	// In the ListMultipartUploads response, the multipart uploads aren't sorted
	//   lexicographically based on the object keys.
	KeyMarker *string

	// Sets the maximum number of multipart uploads, from 1 to 1,000, to return in the
	// response body. 1,000 is the maximum number of uploads that can be returned in a
	// response.
	MaxUploads *int32

	// Lists in-progress uploads only for those keys that begin with the specified
	// prefix. You can use prefixes to separate a bucket into different grouping of
	// keys. (You can think of using prefix to make groups in the same way that you'd
	// use a folder in a file system.)
	//
	// Directory buckets - For directory buckets, only prefixes that end in a
	// delimiter ( / ) are supported.
	Prefix *string

	// Confirms that the requester knows that they will be charged for the request.
	// Bucket owners need not specify this parameter in their requests. If either the
	// source or destination S3 bucket has Requester Pays enabled, the requester will
	// pay for corresponding charges to copy the object. For information about
	// downloading objects from Requester Pays buckets, see [Downloading Objects in Requester Pays Buckets]in the Amazon S3 User
	// Guide.
	//
	// This functionality is not supported for directory buckets.
	//
	// [Downloading Objects in Requester Pays Buckets]: https://docs.aws.amazon.com/AmazonS3/latest/dev/ObjectsinRequesterPaysBuckets.html
	RequestPayer types.RequestPayer

	// Together with key-marker, specifies the multipart upload after which listing
	// should begin. If key-marker is not specified, the upload-id-marker parameter is
	// ignored. Otherwise, any multipart uploads for a key equal to the key-marker
	// might be included in the list only if they have an upload ID lexicographically
	// greater than the specified upload-id-marker .
	//
	// This functionality is not supported for directory buckets.
	UploadIdMarker *string

	noSmithyDocumentSerde
}

func (in *ListMultipartUploadsInput) bindEndpointParams(p *EndpointParameters) {

	p.Bucket = in.Bucket
	p.Prefix = in.Prefix

}

type ListMultipartUploadsOutput struct {

	// The name of the bucket to which the multipart upload was initiated. Does not
	// return the access point ARN or access point alias if used.
	Bucket *string

	// If you specify a delimiter in the request, then the result returns each
	// distinct key prefix containing the delimiter in a CommonPrefixes element. The
	// distinct key prefixes are returned in the Prefix child element.
	//
	// Directory buckets - For directory buckets, only prefixes that end in a
	// delimiter ( / ) are supported.
	CommonPrefixes []types.CommonPrefix

	// Contains the delimiter you specified in the request. If you don't specify a
	// delimiter in your request, this element is absent from the response.
	//
	// Directory buckets - For directory buckets, / is the only supported delimiter.
	Delimiter *string

	// Encoding type used by Amazon S3 to encode object keys in the response.
	//
	// If you specify the encoding-type request parameter, Amazon S3 includes this
	// element in the response, and returns encoded key name values in the following
	// response elements:
	//
	// Delimiter , KeyMarker , Prefix , NextKeyMarker , Key .
	EncodingType types.EncodingType

	// Indicates whether the returned list of multipart uploads is truncated. A value
	// of true indicates that the list was truncated. The list can be truncated if the
	// number of multipart uploads exceeds the limit allowed or specified by max
	// uploads.
	IsTruncated *bool

	// The key at or after which the listing began.
	KeyMarker *string

	// Maximum number of multipart uploads that could have been included in the
	// response.
	MaxUploads *int32

	// When a list is truncated, this element specifies the value that should be used
	// for the key-marker request parameter in a subsequent request.
	NextKeyMarker *string

	// When a list is truncated, this element specifies the value that should be used
	// for the upload-id-marker request parameter in a subsequent request.
	//
	// This functionality is not supported for directory buckets.
	NextUploadIdMarker *string

	// When a prefix is provided in the request, this field contains the specified
	// prefix. The result contains only keys starting with the specified prefix.
	//
	// Directory buckets - For directory buckets, only prefixes that end in a
	// delimiter ( / ) are supported.
	Prefix *string

	// If present, indicates that the requester was successfully charged for the
	// request.
	//
	// This functionality is not supported for directory buckets.
	RequestCharged types.RequestCharged

	// Together with key-marker, specifies the multipart upload after which listing
	// should begin. If key-marker is not specified, the upload-id-marker parameter is
	// ignored. Otherwise, any multipart uploads for a key equal to the key-marker
	// might be included in the list only if they have an upload ID lexicographically
	// greater than the specified upload-id-marker .
	//
	// This functionality is not supported for directory buckets.
	UploadIdMarker *string

	// Container for elements related to a particular multipart upload. A response can
	// contain zero or more Upload elements.
	Uploads []types.MultipartUpload

	// Metadata pertaining to the operation's result.
	ResultMetadata middleware.Metadata

	noSmithyDocumentSerde
}

func (c *Client) addOperationListMultipartUploadsMiddlewares(stack *middleware.Stack, options Options) (err error) {
	if err := stack.Serialize.Add(&setOperationInputMiddleware{}, middleware.After); err != nil {
		return err
	}
	err = stack.Serialize.Add(&awsRestxml_serializeOpListMultipartUploads{}, middleware.After)
	if err != nil {
		return err
	}
	err = stack.Deserialize.Add(&awsRestxml_deserializeOpListMultipartUploads{}, middleware.After)
	if err != nil {
		return err
	}
	if err := addProtocolFinalizerMiddlewares(stack, options, "ListMultipartUploads"); err != nil {
		return fmt.Errorf("add protocol finalizers: %v", err)
	}

	if err = addlegacyEndpointContextSetter(stack, options); err != nil {
		return err
	}
	if err = addSetLoggerMiddleware(stack, options); err != nil {
		return err
	}
	if err = addClientRequestID(stack); err != nil {
		return err
	}
	if err = addComputeContentLength(stack); err != nil {
		return err
	}
	if err = addResolveEndpointMiddleware(stack, options); err != nil {
		return err
	}
	if err = addComputePayloadSHA256(stack); err != nil {
		return err
	}
	if err = addRetry(stack, options); err != nil {
		return err
	}
	if err = addRawResponseToMetadata(stack); err != nil {
		return err
	}
	if err = addRecordResponseTiming(stack); err != nil {
		return err
	}
	if err = addSpanRetryLoop(stack, options); err != nil {
		return err
	}
	if err = addClientUserAgent(stack, options); err != nil {
		return err
	}
	if err = smithyhttp.AddErrorCloseResponseBodyMiddleware(stack); err != nil {
		return err
	}
	if err = smithyhttp.AddCloseResponseBodyMiddleware(stack); err != nil {
		return err
	}
	if err = addSetLegacyContextSigningOptionsMiddleware(stack); err != nil {
		return err
	}
	if err = addPutBucketContextMiddleware(stack); err != nil {
		return err
	}
	if err = addTimeOffsetBuild(stack, c); err != nil {
		return err
	}
	if err = addUserAgentRetryMode(stack, options); err != nil {
		return err
	}
	if err = addIsExpressUserAgent(stack); err != nil {
		return err
	}
	if err = addOpListMultipartUploadsValidationMiddleware(stack); err != nil {
		return err
	}
	if err = stack.Initialize.Add(newServiceMetadataMiddleware_opListMultipartUploads(options.Region), middleware.Before); err != nil {
		return err
	}
	if err = addMetadataRetrieverMiddleware(stack); err != nil {
		return err
	}
	if err = addRecursionDetection(stack); err != nil {
		return err
	}
	if err = addListMultipartUploadsUpdateEndpoint(stack, options); err != nil {
		return err
	}
	if err = addResponseErrorMiddleware(stack); err != nil {
		return err
	}
	if err = v4.AddContentSHA256HeaderMiddleware(stack); err != nil {
		return err
	}
	if err = disableAcceptEncodingGzip(stack); err != nil {
		return err
	}
	if err = addRequestResponseLogging(stack, options); err != nil {
		return err
	}
	if err = addDisableHTTPSMiddleware(stack, options); err != nil {
		return err
	}
	if err = addSerializeImmutableHostnameBucketMiddleware(stack, options); err != nil {
		return err
	}
	if err = addSpanInitializeStart(stack); err != nil {
		return err
	}
	if err = addSpanInitializeEnd(stack); err != nil {
		return err
	}
	if err = addSpanBuildRequestStart(stack); err != nil {
		return err
	}
	if err = addSpanBuildRequestEnd(stack); err != nil {
		return err
	}
	return nil
}

func (v *ListMultipartUploadsInput) bucket() (string, bool) {
	if v.Bucket == nil {
		return "", false
	}
	return *v.Bucket, true
}

func newServiceMetadataMiddleware_opListMultipartUploads(region string) *awsmiddleware.RegisterServiceMetadata {
	return &awsmiddleware.RegisterServiceMetadata{
		Region:        region,
		ServiceID:     ServiceID,
		OperationName: "ListMultipartUploads",
	}
}

// getListMultipartUploadsBucketMember returns a pointer to string denoting a
// provided bucket member valueand a boolean indicating if the input has a modeled
// bucket name,
func getListMultipartUploadsBucketMember(input interface{}) (*string, bool) {
	in := input.(*ListMultipartUploadsInput)
	if in.Bucket == nil {
		return nil, false
	}
	return in.Bucket, true
}
func addListMultipartUploadsUpdateEndpoint(stack *middleware.Stack, options Options) error {
	return s3cust.UpdateEndpoint(stack, s3cust.UpdateEndpointOptions{
		Accessor: s3cust.UpdateEndpointParameterAccessor{
			GetBucketFromInput: getListMultipartUploadsBucketMember,
		},
		UsePathStyle:                   options.UsePathStyle,
		UseAccelerate:                  options.UseAccelerate,
		SupportsAccelerate:             true,
		TargetS3ObjectLambda:           false,
		EndpointResolver:               options.EndpointResolver,
		EndpointResolverOptions:        options.EndpointOptions,
		UseARNRegion:                   options.UseARNRegion,
		DisableMultiRegionAccessPoints: options.DisableMultiRegionAccessPoints,
	})
}
