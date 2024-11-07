// Code generated by smithy-go-codegen DO NOT EDIT.

package s3

import (
	"context"
	"fmt"
	awsmiddleware "github.com/aws/aws-sdk-go-v2/aws/middleware"
	"github.com/aws/aws-sdk-go-v2/aws/signer/v4"
	internalChecksum "github.com/aws/aws-sdk-go-v2/service/internal/checksum"
	s3cust "github.com/aws/aws-sdk-go-v2/service/s3/internal/customizations"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
	"github.com/aws/smithy-go/middleware"
	smithyhttp "github.com/aws/smithy-go/transport/http"
)

// This operation is not supported by directory buckets.
//
// Sets the supplied tag-set to an object that already exists in a bucket. A tag
// is a key-value pair. For more information, see [Object Tagging].
//
// You can associate tags with an object by sending a PUT request against the
// tagging subresource that is associated with the object. You can retrieve tags by
// sending a GET request. For more information, see [GetObjectTagging].
//
// For tagging-related restrictions related to characters and encodings, see [Tag Restrictions].
// Note that Amazon S3 limits the maximum number of tags to 10 tags per object.
//
// To use this operation, you must have permission to perform the
// s3:PutObjectTagging action. By default, the bucket owner has this permission and
// can grant this permission to others.
//
// To put tags of any other version, use the versionId query parameter. You also
// need permission for the s3:PutObjectVersionTagging action.
//
// PutObjectTagging has the following special errors. For more Amazon S3 errors
// see, [Error Responses].
//
//   - InvalidTag - The tag provided was not a valid tag. This error can occur if
//     the tag did not pass input validation. For more information, see [Object Tagging].
//
//   - MalformedXML - The XML provided does not match the schema.
//
//   - OperationAborted - A conflicting conditional action is currently in progress
//     against this resource. Please try again.
//
//   - InternalError - The service was unable to apply the provided tag to the
//     object.
//
// The following operations are related to PutObjectTagging :
//
// [GetObjectTagging]
//
// [DeleteObjectTagging]
//
// [Error Responses]: https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html
// [DeleteObjectTagging]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObjectTagging.html
// [Object Tagging]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html
// [Tag Restrictions]: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/allocation-tag-restrictions.html
// [GetObjectTagging]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectTagging.html
func (c *Client) PutObjectTagging(ctx context.Context, params *PutObjectTaggingInput, optFns ...func(*Options)) (*PutObjectTaggingOutput, error) {
	if params == nil {
		params = &PutObjectTaggingInput{}
	}

	result, metadata, err := c.invokeOperation(ctx, "PutObjectTagging", params, optFns, c.addOperationPutObjectTaggingMiddlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*PutObjectTaggingOutput)
	out.ResultMetadata = metadata
	return out, nil
}

type PutObjectTaggingInput struct {

	// The bucket name containing the object.
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
	// S3 on Outposts - When you use this action with Amazon S3 on Outposts, you must
	// direct requests to the S3 on Outposts hostname. The S3 on Outposts hostname
	// takes the form
	// AccessPointName-AccountId.outpostID.s3-outposts.Region.amazonaws.com . When you
	// use this action with S3 on Outposts through the Amazon Web Services SDKs, you
	// provide the Outposts access point ARN in place of the bucket name. For more
	// information about S3 on Outposts ARNs, see [What is S3 on Outposts?]in the Amazon S3 User Guide.
	//
	// [What is S3 on Outposts?]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html
	// [Using access points]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-access-points.html
	//
	// This member is required.
	Bucket *string

	// Name of the object key.
	//
	// This member is required.
	Key *string

	// Container for the TagSet and Tag elements
	//
	// This member is required.
	Tagging *types.Tagging

	// Indicates the algorithm used to create the checksum for the object when you use
	// the SDK. This header will not provide any additional functionality if you don't
	// use the SDK. When you send this header, there must be a corresponding
	// x-amz-checksum or x-amz-trailer header sent. Otherwise, Amazon S3 fails the
	// request with the HTTP status code 400 Bad Request . For more information, see [Checking object integrity]
	// in the Amazon S3 User Guide.
	//
	// If you provide an individual checksum, Amazon S3 ignores any provided
	// ChecksumAlgorithm parameter.
	//
	// [Checking object integrity]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html
	ChecksumAlgorithm types.ChecksumAlgorithm

	// The MD5 hash for the request body.
	//
	// For requests made using the Amazon Web Services Command Line Interface (CLI) or
	// Amazon Web Services SDKs, this field is calculated automatically.
	ContentMD5 *string

	// The account ID of the expected bucket owner. If the account ID that you provide
	// does not match the actual owner of the bucket, the request fails with the HTTP
	// status code 403 Forbidden (access denied).
	ExpectedBucketOwner *string

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

	// The versionId of the object that the tag-set will be added to.
	VersionId *string

	noSmithyDocumentSerde
}

func (in *PutObjectTaggingInput) bindEndpointParams(p *EndpointParameters) {

	p.Bucket = in.Bucket

}

type PutObjectTaggingOutput struct {

	// The versionId of the object the tag-set was added to.
	VersionId *string

	// Metadata pertaining to the operation's result.
	ResultMetadata middleware.Metadata

	noSmithyDocumentSerde
}

func (c *Client) addOperationPutObjectTaggingMiddlewares(stack *middleware.Stack, options Options) (err error) {
	if err := stack.Serialize.Add(&setOperationInputMiddleware{}, middleware.After); err != nil {
		return err
	}
	err = stack.Serialize.Add(&awsRestxml_serializeOpPutObjectTagging{}, middleware.After)
	if err != nil {
		return err
	}
	err = stack.Deserialize.Add(&awsRestxml_deserializeOpPutObjectTagging{}, middleware.After)
	if err != nil {
		return err
	}
	if err := addProtocolFinalizerMiddlewares(stack, options, "PutObjectTagging"); err != nil {
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
	if err = addOpPutObjectTaggingValidationMiddleware(stack); err != nil {
		return err
	}
	if err = stack.Initialize.Add(newServiceMetadataMiddleware_opPutObjectTagging(options.Region), middleware.Before); err != nil {
		return err
	}
	if err = addMetadataRetrieverMiddleware(stack); err != nil {
		return err
	}
	if err = addRecursionDetection(stack); err != nil {
		return err
	}
	if err = addPutObjectTaggingInputChecksumMiddlewares(stack, options); err != nil {
		return err
	}
	if err = addPutObjectTaggingUpdateEndpoint(stack, options); err != nil {
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
	if err = s3cust.AddExpressDefaultChecksumMiddleware(stack); err != nil {
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

func (v *PutObjectTaggingInput) bucket() (string, bool) {
	if v.Bucket == nil {
		return "", false
	}
	return *v.Bucket, true
}

func newServiceMetadataMiddleware_opPutObjectTagging(region string) *awsmiddleware.RegisterServiceMetadata {
	return &awsmiddleware.RegisterServiceMetadata{
		Region:        region,
		ServiceID:     ServiceID,
		OperationName: "PutObjectTagging",
	}
}

// getPutObjectTaggingRequestAlgorithmMember gets the request checksum algorithm
// value provided as input.
func getPutObjectTaggingRequestAlgorithmMember(input interface{}) (string, bool) {
	in := input.(*PutObjectTaggingInput)
	if len(in.ChecksumAlgorithm) == 0 {
		return "", false
	}
	return string(in.ChecksumAlgorithm), true
}

func addPutObjectTaggingInputChecksumMiddlewares(stack *middleware.Stack, options Options) error {
	return internalChecksum.AddInputMiddleware(stack, internalChecksum.InputMiddlewareOptions{
		GetAlgorithm:                     getPutObjectTaggingRequestAlgorithmMember,
		RequireChecksum:                  true,
		EnableTrailingChecksum:           false,
		EnableComputeSHA256PayloadHash:   true,
		EnableDecodedContentLengthHeader: true,
	})
}

// getPutObjectTaggingBucketMember returns a pointer to string denoting a provided
// bucket member valueand a boolean indicating if the input has a modeled bucket
// name,
func getPutObjectTaggingBucketMember(input interface{}) (*string, bool) {
	in := input.(*PutObjectTaggingInput)
	if in.Bucket == nil {
		return nil, false
	}
	return in.Bucket, true
}
func addPutObjectTaggingUpdateEndpoint(stack *middleware.Stack, options Options) error {
	return s3cust.UpdateEndpoint(stack, s3cust.UpdateEndpointOptions{
		Accessor: s3cust.UpdateEndpointParameterAccessor{
			GetBucketFromInput: getPutObjectTaggingBucketMember,
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
