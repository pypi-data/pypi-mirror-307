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

// Returns some or all (up to 1,000) of the objects in a bucket with each request.
// You can use the request parameters as selection criteria to return a subset of
// the objects in a bucket. A 200 OK response can contain valid or invalid XML.
// Make sure to design your application to parse the contents of the response and
// handle it appropriately.
//
// For more information about listing objects, see [Listing object keys programmatically] in the Amazon S3 User Guide.
// To get a list of your buckets, see [ListBuckets].
//
//   - General purpose bucket - For general purpose buckets, ListObjectsV2 doesn't
//     return prefixes that are related only to in-progress multipart uploads.
//
//   - Directory buckets - For directory buckets, ListObjectsV2 response includes
//     the prefixes that are related only to in-progress multipart uploads.
//
//   - Directory buckets - For directory buckets, you must make requests for this
//     API operation to the Zonal endpoint. These endpoints support
//     virtual-hosted-style requests in the format
//     https://bucket_name.s3express-az_id.region.amazonaws.com/key-name .
//     Path-style requests are not supported. For more information, see [Regional and Zonal endpoints]in the
//     Amazon S3 User Guide.
//
// Permissions
//
//   - General purpose bucket permissions - To use this operation, you must have
//     READ access to the bucket. You must have permission to perform the
//     s3:ListBucket action. The bucket owner has this permission by default and can
//     grant this permission to others. For more information about permissions, see [Permissions Related to Bucket Subresource Operations]
//     and [Managing Access Permissions to Your Amazon S3 Resources]in the Amazon S3 User Guide.
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
// Sorting order of returned objects
//
//   - General purpose bucket - For general purpose buckets, ListObjectsV2 returns
//     objects in lexicographical order based on their key names.
//
//   - Directory bucket - For directory buckets, ListObjectsV2 does not return
//     objects in lexicographical order.
//
// HTTP Host header syntax  Directory buckets - The HTTP Host header syntax is
// Bucket_name.s3express-az_id.region.amazonaws.com .
//
// This section describes the latest revision of this action. We recommend that
// you use this revised API operation for application development. For backward
// compatibility, Amazon S3 continues to support the prior version of this API
// operation, [ListObjects].
//
// The following operations are related to ListObjectsV2 :
//
// [GetObject]
//
// [PutObject]
//
// [CreateBucket]
//
// [ListObjects]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjects.html
// [Permissions Related to Bucket Subresource Operations]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources
// [Listing object keys programmatically]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html
// [Regional and Zonal endpoints]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-Regions-and-Zones.html
// [ListBuckets]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html
// [PutObject]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html
// [Managing Access Permissions to Your Amazon S3 Resources]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html
// [CreateSession]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateSession.html
// [GetObject]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
// [CreateBucket]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html
func (c *Client) ListObjectsV2(ctx context.Context, params *ListObjectsV2Input, optFns ...func(*Options)) (*ListObjectsV2Output, error) {
	if params == nil {
		params = &ListObjectsV2Input{}
	}

	result, metadata, err := c.invokeOperation(ctx, "ListObjectsV2", params, optFns, c.addOperationListObjectsV2Middlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*ListObjectsV2Output)
	out.ResultMetadata = metadata
	return out, nil
}

type ListObjectsV2Input struct {

	//  Directory buckets - When you use this operation with a directory bucket, you
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

	// ContinuationToken indicates to Amazon S3 that the list is being continued on
	// this bucket with a token. ContinuationToken is obfuscated and is not a real
	// key. You can use this ContinuationToken for pagination of the list results.
	ContinuationToken *string

	// A delimiter is a character that you use to group keys.
	//
	//   - Directory buckets - For directory buckets, / is the only supported delimiter.
	//
	//   - Directory buckets - When you query ListObjectsV2 with a delimiter during
	//   in-progress multipart uploads, the CommonPrefixes response parameter contains
	//   the prefixes that are associated with the in-progress multipart uploads. For
	//   more information about multipart uploads, see [Multipart Upload Overview]in the Amazon S3 User Guide.
	//
	// [Multipart Upload Overview]: https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html
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

	// The owner field is not present in ListObjectsV2 by default. If you want to
	// return the owner field with each key in the result, then set the FetchOwner
	// field to true .
	//
	// Directory buckets - For directory buckets, the bucket owner is returned as the
	// object owner for all objects.
	FetchOwner *bool

	// Sets the maximum number of keys returned in the response. By default, the
	// action returns up to 1,000 key names. The response might contain fewer keys but
	// will never contain more.
	MaxKeys *int32

	// Specifies the optional fields that you want returned in the response. Fields
	// that you do not specify are not returned.
	//
	// This functionality is not supported for directory buckets.
	OptionalObjectAttributes []types.OptionalObjectAttributes

	// Limits the response to keys that begin with the specified prefix.
	//
	// Directory buckets - For directory buckets, only prefixes that end in a
	// delimiter ( / ) are supported.
	Prefix *string

	// Confirms that the requester knows that she or he will be charged for the list
	// objects request in V2 style. Bucket owners need not specify this parameter in
	// their requests.
	//
	// This functionality is not supported for directory buckets.
	RequestPayer types.RequestPayer

	// StartAfter is where you want Amazon S3 to start listing from. Amazon S3 starts
	// listing after this specified key. StartAfter can be any key in the bucket.
	//
	// This functionality is not supported for directory buckets.
	StartAfter *string

	noSmithyDocumentSerde
}

func (in *ListObjectsV2Input) bindEndpointParams(p *EndpointParameters) {

	p.Bucket = in.Bucket
	p.Prefix = in.Prefix

}

type ListObjectsV2Output struct {

	// All of the keys (up to 1,000) that share the same prefix are grouped together.
	// When counting the total numbers of returns by this API operation, this group of
	// keys is considered as one item.
	//
	// A response can contain CommonPrefixes only if you specify a delimiter.
	//
	// CommonPrefixes contains all (if there are any) keys between Prefix and the next
	// occurrence of the string specified by a delimiter.
	//
	// CommonPrefixes lists keys that act like subdirectories in the directory
	// specified by Prefix .
	//
	// For example, if the prefix is notes/ and the delimiter is a slash ( / ) as in
	// notes/summer/july , the common prefix is notes/summer/ . All of the keys that
	// roll up into a common prefix count as a single return when calculating the
	// number of returns.
	//
	//   - Directory buckets - For directory buckets, only prefixes that end in a
	//   delimiter ( / ) are supported.
	//
	//   - Directory buckets - When you query ListObjectsV2 with a delimiter during
	//   in-progress multipart uploads, the CommonPrefixes response parameter contains
	//   the prefixes that are associated with the in-progress multipart uploads. For
	//   more information about multipart uploads, see [Multipart Upload Overview]in the Amazon S3 User Guide.
	//
	// [Multipart Upload Overview]: https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html
	CommonPrefixes []types.CommonPrefix

	// Metadata about each object returned.
	Contents []types.Object

	//  If ContinuationToken was sent with the request, it is included in the
	// response. You can use the returned ContinuationToken for pagination of the list
	// response. You can use this ContinuationToken for pagination of the list
	// results.
	ContinuationToken *string

	// Causes keys that contain the same string between the prefix and the first
	// occurrence of the delimiter to be rolled up into a single result element in the
	// CommonPrefixes collection. These rolled-up keys are not returned elsewhere in
	// the response. Each rolled-up result counts as only one return against the
	// MaxKeys value.
	//
	// Directory buckets - For directory buckets, / is the only supported delimiter.
	Delimiter *string

	// Encoding type used by Amazon S3 to encode object key names in the XML response.
	//
	// If you specify the encoding-type request parameter, Amazon S3 includes this
	// element in the response, and returns encoded key name values in the following
	// response elements:
	//
	// Delimiter, Prefix, Key, and StartAfter .
	EncodingType types.EncodingType

	// Set to false if all of the results were returned. Set to true if more keys are
	// available to return. If the number of results exceeds that specified by MaxKeys
	// , all of the results might not be returned.
	IsTruncated *bool

	// KeyCount is the number of keys returned with this request. KeyCount will always
	// be less than or equal to the MaxKeys field. For example, if you ask for 50
	// keys, your result will include 50 keys or fewer.
	KeyCount *int32

	// Sets the maximum number of keys returned in the response. By default, the
	// action returns up to 1,000 key names. The response might contain fewer keys but
	// will never contain more.
	MaxKeys *int32

	// The bucket name.
	Name *string

	// NextContinuationToken is sent when isTruncated is true, which means there are
	// more keys in the bucket that can be listed. The next list requests to Amazon S3
	// can be continued with this NextContinuationToken . NextContinuationToken is
	// obfuscated and is not a real key
	NextContinuationToken *string

	// Keys that begin with the indicated prefix.
	//
	// Directory buckets - For directory buckets, only prefixes that end in a
	// delimiter ( / ) are supported.
	Prefix *string

	// If present, indicates that the requester was successfully charged for the
	// request.
	//
	// This functionality is not supported for directory buckets.
	RequestCharged types.RequestCharged

	// If StartAfter was sent with the request, it is included in the response.
	//
	// This functionality is not supported for directory buckets.
	StartAfter *string

	// Metadata pertaining to the operation's result.
	ResultMetadata middleware.Metadata

	noSmithyDocumentSerde
}

func (c *Client) addOperationListObjectsV2Middlewares(stack *middleware.Stack, options Options) (err error) {
	if err := stack.Serialize.Add(&setOperationInputMiddleware{}, middleware.After); err != nil {
		return err
	}
	err = stack.Serialize.Add(&awsRestxml_serializeOpListObjectsV2{}, middleware.After)
	if err != nil {
		return err
	}
	err = stack.Deserialize.Add(&awsRestxml_deserializeOpListObjectsV2{}, middleware.After)
	if err != nil {
		return err
	}
	if err := addProtocolFinalizerMiddlewares(stack, options, "ListObjectsV2"); err != nil {
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
	if err = addOpListObjectsV2ValidationMiddleware(stack); err != nil {
		return err
	}
	if err = stack.Initialize.Add(newServiceMetadataMiddleware_opListObjectsV2(options.Region), middleware.Before); err != nil {
		return err
	}
	if err = addMetadataRetrieverMiddleware(stack); err != nil {
		return err
	}
	if err = addRecursionDetection(stack); err != nil {
		return err
	}
	if err = addListObjectsV2UpdateEndpoint(stack, options); err != nil {
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

// ListObjectsV2PaginatorOptions is the paginator options for ListObjectsV2
type ListObjectsV2PaginatorOptions struct {
	// Sets the maximum number of keys returned in the response. By default, the
	// action returns up to 1,000 key names. The response might contain fewer keys but
	// will never contain more.
	Limit int32

	// Set to true if pagination should stop if the service returns a pagination token
	// that matches the most recent token provided to the service.
	StopOnDuplicateToken bool
}

// ListObjectsV2Paginator is a paginator for ListObjectsV2
type ListObjectsV2Paginator struct {
	options   ListObjectsV2PaginatorOptions
	client    ListObjectsV2APIClient
	params    *ListObjectsV2Input
	nextToken *string
	firstPage bool
}

// NewListObjectsV2Paginator returns a new ListObjectsV2Paginator
func NewListObjectsV2Paginator(client ListObjectsV2APIClient, params *ListObjectsV2Input, optFns ...func(*ListObjectsV2PaginatorOptions)) *ListObjectsV2Paginator {
	if params == nil {
		params = &ListObjectsV2Input{}
	}

	options := ListObjectsV2PaginatorOptions{}
	if params.MaxKeys != nil {
		options.Limit = *params.MaxKeys
	}

	for _, fn := range optFns {
		fn(&options)
	}

	return &ListObjectsV2Paginator{
		options:   options,
		client:    client,
		params:    params,
		firstPage: true,
		nextToken: params.ContinuationToken,
	}
}

// HasMorePages returns a boolean indicating whether more pages are available
func (p *ListObjectsV2Paginator) HasMorePages() bool {
	return p.firstPage || (p.nextToken != nil && len(*p.nextToken) != 0)
}

// NextPage retrieves the next ListObjectsV2 page.
func (p *ListObjectsV2Paginator) NextPage(ctx context.Context, optFns ...func(*Options)) (*ListObjectsV2Output, error) {
	if !p.HasMorePages() {
		return nil, fmt.Errorf("no more pages available")
	}

	params := *p.params
	params.ContinuationToken = p.nextToken

	var limit *int32
	if p.options.Limit > 0 {
		limit = &p.options.Limit
	}
	params.MaxKeys = limit

	optFns = append([]func(*Options){
		addIsPaginatorUserAgent,
	}, optFns...)
	result, err := p.client.ListObjectsV2(ctx, &params, optFns...)
	if err != nil {
		return nil, err
	}
	p.firstPage = false

	prevToken := p.nextToken
	p.nextToken = nil
	if result.IsTruncated != nil && *result.IsTruncated {
		p.nextToken = result.NextContinuationToken
	}

	if p.options.StopOnDuplicateToken &&
		prevToken != nil &&
		p.nextToken != nil &&
		*prevToken == *p.nextToken {
		p.nextToken = nil
	}

	return result, nil
}

func (v *ListObjectsV2Input) bucket() (string, bool) {
	if v.Bucket == nil {
		return "", false
	}
	return *v.Bucket, true
}

// ListObjectsV2APIClient is a client that implements the ListObjectsV2 operation.
type ListObjectsV2APIClient interface {
	ListObjectsV2(context.Context, *ListObjectsV2Input, ...func(*Options)) (*ListObjectsV2Output, error)
}

var _ ListObjectsV2APIClient = (*Client)(nil)

func newServiceMetadataMiddleware_opListObjectsV2(region string) *awsmiddleware.RegisterServiceMetadata {
	return &awsmiddleware.RegisterServiceMetadata{
		Region:        region,
		ServiceID:     ServiceID,
		OperationName: "ListObjectsV2",
	}
}

// getListObjectsV2BucketMember returns a pointer to string denoting a provided
// bucket member valueand a boolean indicating if the input has a modeled bucket
// name,
func getListObjectsV2BucketMember(input interface{}) (*string, bool) {
	in := input.(*ListObjectsV2Input)
	if in.Bucket == nil {
		return nil, false
	}
	return in.Bucket, true
}
func addListObjectsV2UpdateEndpoint(stack *middleware.Stack, options Options) error {
	return s3cust.UpdateEndpoint(stack, s3cust.UpdateEndpointOptions{
		Accessor: s3cust.UpdateEndpointParameterAccessor{
			GetBucketFromInput: getListObjectsV2BucketMember,
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
