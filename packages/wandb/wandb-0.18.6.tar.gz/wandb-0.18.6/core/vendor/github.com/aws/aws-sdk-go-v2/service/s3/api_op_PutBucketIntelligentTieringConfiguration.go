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
	"github.com/aws/smithy-go/ptr"
	smithyhttp "github.com/aws/smithy-go/transport/http"
)

// This operation is not supported by directory buckets.
//
// Puts a S3 Intelligent-Tiering configuration to the specified bucket. You can
// have up to 1,000 S3 Intelligent-Tiering configurations per bucket.
//
// The S3 Intelligent-Tiering storage class is designed to optimize storage costs
// by automatically moving data to the most cost-effective storage access tier,
// without performance impact or operational overhead. S3 Intelligent-Tiering
// delivers automatic cost savings in three low latency and high throughput access
// tiers. To get the lowest storage cost on data that can be accessed in minutes to
// hours, you can choose to activate additional archiving capabilities.
//
// The S3 Intelligent-Tiering storage class is the ideal storage class for data
// with unknown, changing, or unpredictable access patterns, independent of object
// size or retention period. If the size of an object is less than 128 KB, it is
// not monitored and not eligible for auto-tiering. Smaller objects can be stored,
// but they are always charged at the Frequent Access tier rates in the S3
// Intelligent-Tiering storage class.
//
// For more information, see [Storage class for automatically optimizing frequently and infrequently accessed objects].
//
// Operations related to PutBucketIntelligentTieringConfiguration include:
//
// [DeleteBucketIntelligentTieringConfiguration]
//
// [GetBucketIntelligentTieringConfiguration]
//
// [ListBucketIntelligentTieringConfigurations]
//
// You only need S3 Intelligent-Tiering enabled on a bucket if you want to
// automatically move objects stored in the S3 Intelligent-Tiering storage class to
// the Archive Access or Deep Archive Access tier.
//
// PutBucketIntelligentTieringConfiguration has the following special errors:
//
// HTTP 400 Bad Request Error  Code: InvalidArgument
//
// Cause: Invalid Argument
//
// HTTP 400 Bad Request Error  Code: TooManyConfigurations
//
// Cause: You are attempting to create a new configuration but have already
// reached the 1,000-configuration limit.
//
// HTTP 403 Forbidden Error  Cause: You are not the owner of the specified bucket,
// or you do not have the s3:PutIntelligentTieringConfiguration bucket permission
// to set the configuration on the bucket.
//
// [ListBucketIntelligentTieringConfigurations]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBucketIntelligentTieringConfigurations.html
// [GetBucketIntelligentTieringConfiguration]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketIntelligentTieringConfiguration.html
// [Storage class for automatically optimizing frequently and infrequently accessed objects]: https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html#sc-dynamic-data-access
// [DeleteBucketIntelligentTieringConfiguration]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketIntelligentTieringConfiguration.html
func (c *Client) PutBucketIntelligentTieringConfiguration(ctx context.Context, params *PutBucketIntelligentTieringConfigurationInput, optFns ...func(*Options)) (*PutBucketIntelligentTieringConfigurationOutput, error) {
	if params == nil {
		params = &PutBucketIntelligentTieringConfigurationInput{}
	}

	result, metadata, err := c.invokeOperation(ctx, "PutBucketIntelligentTieringConfiguration", params, optFns, c.addOperationPutBucketIntelligentTieringConfigurationMiddlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*PutBucketIntelligentTieringConfigurationOutput)
	out.ResultMetadata = metadata
	return out, nil
}

type PutBucketIntelligentTieringConfigurationInput struct {

	// The name of the Amazon S3 bucket whose configuration you want to modify or
	// retrieve.
	//
	// This member is required.
	Bucket *string

	// The ID used to identify the S3 Intelligent-Tiering configuration.
	//
	// This member is required.
	Id *string

	// Container for S3 Intelligent-Tiering configuration.
	//
	// This member is required.
	IntelligentTieringConfiguration *types.IntelligentTieringConfiguration

	noSmithyDocumentSerde
}

func (in *PutBucketIntelligentTieringConfigurationInput) bindEndpointParams(p *EndpointParameters) {

	p.Bucket = in.Bucket
	p.UseS3ExpressControlEndpoint = ptr.Bool(true)
}

type PutBucketIntelligentTieringConfigurationOutput struct {
	// Metadata pertaining to the operation's result.
	ResultMetadata middleware.Metadata

	noSmithyDocumentSerde
}

func (c *Client) addOperationPutBucketIntelligentTieringConfigurationMiddlewares(stack *middleware.Stack, options Options) (err error) {
	if err := stack.Serialize.Add(&setOperationInputMiddleware{}, middleware.After); err != nil {
		return err
	}
	err = stack.Serialize.Add(&awsRestxml_serializeOpPutBucketIntelligentTieringConfiguration{}, middleware.After)
	if err != nil {
		return err
	}
	err = stack.Deserialize.Add(&awsRestxml_deserializeOpPutBucketIntelligentTieringConfiguration{}, middleware.After)
	if err != nil {
		return err
	}
	if err := addProtocolFinalizerMiddlewares(stack, options, "PutBucketIntelligentTieringConfiguration"); err != nil {
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
	if err = addOpPutBucketIntelligentTieringConfigurationValidationMiddleware(stack); err != nil {
		return err
	}
	if err = stack.Initialize.Add(newServiceMetadataMiddleware_opPutBucketIntelligentTieringConfiguration(options.Region), middleware.Before); err != nil {
		return err
	}
	if err = addMetadataRetrieverMiddleware(stack); err != nil {
		return err
	}
	if err = addRecursionDetection(stack); err != nil {
		return err
	}
	if err = addPutBucketIntelligentTieringConfigurationUpdateEndpoint(stack, options); err != nil {
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

func (v *PutBucketIntelligentTieringConfigurationInput) bucket() (string, bool) {
	if v.Bucket == nil {
		return "", false
	}
	return *v.Bucket, true
}

func newServiceMetadataMiddleware_opPutBucketIntelligentTieringConfiguration(region string) *awsmiddleware.RegisterServiceMetadata {
	return &awsmiddleware.RegisterServiceMetadata{
		Region:        region,
		ServiceID:     ServiceID,
		OperationName: "PutBucketIntelligentTieringConfiguration",
	}
}

// getPutBucketIntelligentTieringConfigurationBucketMember returns a pointer to
// string denoting a provided bucket member valueand a boolean indicating if the
// input has a modeled bucket name,
func getPutBucketIntelligentTieringConfigurationBucketMember(input interface{}) (*string, bool) {
	in := input.(*PutBucketIntelligentTieringConfigurationInput)
	if in.Bucket == nil {
		return nil, false
	}
	return in.Bucket, true
}
func addPutBucketIntelligentTieringConfigurationUpdateEndpoint(stack *middleware.Stack, options Options) error {
	return s3cust.UpdateEndpoint(stack, s3cust.UpdateEndpointOptions{
		Accessor: s3cust.UpdateEndpointParameterAccessor{
			GetBucketFromInput: getPutBucketIntelligentTieringConfigurationBucketMember,
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
