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
	smithysync "github.com/aws/smithy-go/sync"
	"sync"
)

// This operation is not supported by directory buckets.
//
// This action filters the contents of an Amazon S3 object based on a simple
// structured query language (SQL) statement. In the request, along with the SQL
// expression, you must also specify a data serialization format (JSON, CSV, or
// Apache Parquet) of the object. Amazon S3 uses this format to parse object data
// into records, and returns only records that match the specified SQL expression.
// You must also specify the data serialization format for the response.
//
// This functionality is not supported for Amazon S3 on Outposts.
//
// For more information about Amazon S3 Select, see [Selecting Content from Objects] and [SELECT Command] in the Amazon S3 User
// Guide.
//
// Permissions You must have the s3:GetObject permission for this operation.
// Amazon S3 Select does not support anonymous access. For more information about
// permissions, see [Specifying Permissions in a Policy]in the Amazon S3 User Guide.
//
// Object Data Formats You can use Amazon S3 Select to query objects that have the
// following format properties:
//
//   - CSV, JSON, and Parquet - Objects must be in CSV, JSON, or Parquet format.
//
//   - UTF-8 - UTF-8 is the only encoding type Amazon S3 Select supports.
//
//   - GZIP or BZIP2 - CSV and JSON files can be compressed using GZIP or BZIP2.
//     GZIP and BZIP2 are the only compression formats that Amazon S3 Select supports
//     for CSV and JSON files. Amazon S3 Select supports columnar compression for
//     Parquet using GZIP or Snappy. Amazon S3 Select does not support whole-object
//     compression for Parquet objects.
//
//   - Server-side encryption - Amazon S3 Select supports querying objects that
//     are protected with server-side encryption.
//
// For objects that are encrypted with customer-provided encryption keys (SSE-C),
//
//	you must use HTTPS, and you must use the headers that are documented in the [GetObject].
//	For more information about SSE-C, see [Server-Side Encryption (Using Customer-Provided Encryption Keys)]in the Amazon S3 User Guide.
//
// For objects that are encrypted with Amazon S3 managed keys (SSE-S3) and Amazon
//
//	Web Services KMS keys (SSE-KMS), server-side encryption is handled
//	transparently, so you don't need to specify anything. For more information about
//	server-side encryption, including SSE-S3 and SSE-KMS, see [Protecting Data Using Server-Side Encryption]in the Amazon S3
//	User Guide.
//
// Working with the Response Body Given the response size is unknown, Amazon S3
// Select streams the response as a series of messages and includes a
// Transfer-Encoding header with chunked as its value in the response. For more
// information, see [Appendix: SelectObjectContent Response].
//
// GetObject Support The SelectObjectContent action does not support the following
// GetObject functionality. For more information, see [GetObject].
//
//   - Range : Although you can specify a scan range for an Amazon S3 Select
//     request (see [SelectObjectContentRequest - ScanRange]in the request parameters), you cannot specify the range of
//     bytes of an object to return.
//
//   - The GLACIER , DEEP_ARCHIVE , and REDUCED_REDUNDANCY storage classes, or the
//     ARCHIVE_ACCESS and DEEP_ARCHIVE_ACCESS access tiers of the INTELLIGENT_TIERING
//     storage class: You cannot query objects in the GLACIER , DEEP_ARCHIVE , or
//     REDUCED_REDUNDANCY storage classes, nor objects in the ARCHIVE_ACCESS or
//     DEEP_ARCHIVE_ACCESS access tiers of the INTELLIGENT_TIERING storage class. For
//     more information about storage classes, see [Using Amazon S3 storage classes]in the Amazon S3 User Guide.
//
// Special Errors For a list of special errors for this operation, see [List of SELECT Object Content Error Codes]
//
// The following operations are related to SelectObjectContent :
//
// [GetObject]
//
// [GetBucketLifecycleConfiguration]
//
// [PutBucketLifecycleConfiguration]
//
// [Appendix: SelectObjectContent Response]: https://docs.aws.amazon.com/AmazonS3/latest/API/RESTSelectObjectAppendix.html
// [Selecting Content from Objects]: https://docs.aws.amazon.com/AmazonS3/latest/dev/selecting-content-from-objects.html
// [PutBucketLifecycleConfiguration]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html
// [SelectObjectContentRequest - ScanRange]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html#AmazonS3-SelectObjectContent-request-ScanRange
// [List of SELECT Object Content Error Codes]: https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html#SelectObjectContentErrorCodeList
// [GetBucketLifecycleConfiguration]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLifecycleConfiguration.html
// [Using Amazon S3 storage classes]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html
// [SELECT Command]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-glacier-select-sql-reference-select.html
// [GetObject]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
// [Specifying Permissions in a Policy]: https://docs.aws.amazon.com/AmazonS3/latest/dev/using-with-s3-actions.html
//
// [Server-Side Encryption (Using Customer-Provided Encryption Keys)]: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html
// [Protecting Data Using Server-Side Encryption]: https://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html
func (c *Client) SelectObjectContent(ctx context.Context, params *SelectObjectContentInput, optFns ...func(*Options)) (*SelectObjectContentOutput, error) {
	if params == nil {
		params = &SelectObjectContentInput{}
	}

	result, metadata, err := c.invokeOperation(ctx, "SelectObjectContent", params, optFns, c.addOperationSelectObjectContentMiddlewares)
	if err != nil {
		return nil, err
	}

	out := result.(*SelectObjectContentOutput)
	out.ResultMetadata = metadata
	return out, nil
}

// Request to filter the contents of an Amazon S3 object based on a simple
// Structured Query Language (SQL) statement. In the request, along with the SQL
// expression, you must specify a data serialization format (JSON or CSV) of the
// object. Amazon S3 uses this to parse object data into records. It returns only
// records that match the specified SQL expression. You must also specify the data
// serialization format for the response. For more information, see [S3Select API Documentation].
//
// [S3Select API Documentation]: https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectSELECTContent.html
type SelectObjectContentInput struct {

	// The S3 bucket.
	//
	// This member is required.
	Bucket *string

	// The expression that is used to query the object.
	//
	// This member is required.
	Expression *string

	// The type of the provided expression (for example, SQL).
	//
	// This member is required.
	ExpressionType types.ExpressionType

	// Describes the format of the data in the object that is being queried.
	//
	// This member is required.
	InputSerialization *types.InputSerialization

	// The object key.
	//
	// This member is required.
	Key *string

	// Describes the format of the data that you want Amazon S3 to return in response.
	//
	// This member is required.
	OutputSerialization *types.OutputSerialization

	// The account ID of the expected bucket owner. If the account ID that you provide
	// does not match the actual owner of the bucket, the request fails with the HTTP
	// status code 403 Forbidden (access denied).
	ExpectedBucketOwner *string

	// Specifies if periodic request progress information should be enabled.
	RequestProgress *types.RequestProgress

	// The server-side encryption (SSE) algorithm used to encrypt the object. This
	// parameter is needed only when the object was created using a checksum algorithm.
	// For more information, see [Protecting data using SSE-C keys]in the Amazon S3 User Guide.
	//
	// [Protecting data using SSE-C keys]: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html
	SSECustomerAlgorithm *string

	// The server-side encryption (SSE) customer managed key. This parameter is needed
	// only when the object was created using a checksum algorithm. For more
	// information, see [Protecting data using SSE-C keys]in the Amazon S3 User Guide.
	//
	// [Protecting data using SSE-C keys]: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html
	SSECustomerKey *string

	// The MD5 server-side encryption (SSE) customer managed key. This parameter is
	// needed only when the object was created using a checksum algorithm. For more
	// information, see [Protecting data using SSE-C keys]in the Amazon S3 User Guide.
	//
	// [Protecting data using SSE-C keys]: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html
	SSECustomerKeyMD5 *string

	// Specifies the byte range of the object to get the records from. A record is
	// processed when its first byte is contained by the range. This parameter is
	// optional, but when specified, it must not be empty. See RFC 2616, Section
	// 14.35.1 about how to specify the start and end of the range.
	//
	// ScanRange may be used in the following ways:
	//
	//   - 50100 - process only the records starting between the bytes 50 and 100
	//   (inclusive, counting from zero)
	//
	//   - 50 - process only the records starting after the byte 50
	//
	//   - 50 - process only the records within the last 50 bytes of the file.
	ScanRange *types.ScanRange

	noSmithyDocumentSerde
}

func (in *SelectObjectContentInput) bindEndpointParams(p *EndpointParameters) {

	p.Bucket = in.Bucket

}

type SelectObjectContentOutput struct {
	eventStream *SelectObjectContentEventStream

	// Metadata pertaining to the operation's result.
	ResultMetadata middleware.Metadata

	noSmithyDocumentSerde
}

// GetStream returns the type to interact with the event stream.
func (o *SelectObjectContentOutput) GetStream() *SelectObjectContentEventStream {
	return o.eventStream
}

func (c *Client) addOperationSelectObjectContentMiddlewares(stack *middleware.Stack, options Options) (err error) {
	if err := stack.Serialize.Add(&setOperationInputMiddleware{}, middleware.After); err != nil {
		return err
	}
	err = stack.Serialize.Add(&awsRestxml_serializeOpSelectObjectContent{}, middleware.After)
	if err != nil {
		return err
	}
	err = stack.Deserialize.Add(&awsRestxml_deserializeOpSelectObjectContent{}, middleware.After)
	if err != nil {
		return err
	}
	if err := addProtocolFinalizerMiddlewares(stack, options, "SelectObjectContent"); err != nil {
		return fmt.Errorf("add protocol finalizers: %v", err)
	}

	if err = addlegacyEndpointContextSetter(stack, options); err != nil {
		return err
	}
	if err = addEventStreamSelectObjectContentMiddleware(stack, options); err != nil {
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
	if err = addOpSelectObjectContentValidationMiddleware(stack); err != nil {
		return err
	}
	if err = stack.Initialize.Add(newServiceMetadataMiddleware_opSelectObjectContent(options.Region), middleware.Before); err != nil {
		return err
	}
	if err = addMetadataRetrieverMiddleware(stack); err != nil {
		return err
	}
	if err = addRecursionDetection(stack); err != nil {
		return err
	}
	if err = addSelectObjectContentUpdateEndpoint(stack, options); err != nil {
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

func (v *SelectObjectContentInput) bucket() (string, bool) {
	if v.Bucket == nil {
		return "", false
	}
	return *v.Bucket, true
}

func newServiceMetadataMiddleware_opSelectObjectContent(region string) *awsmiddleware.RegisterServiceMetadata {
	return &awsmiddleware.RegisterServiceMetadata{
		Region:        region,
		ServiceID:     ServiceID,
		OperationName: "SelectObjectContent",
	}
}

// getSelectObjectContentBucketMember returns a pointer to string denoting a
// provided bucket member valueand a boolean indicating if the input has a modeled
// bucket name,
func getSelectObjectContentBucketMember(input interface{}) (*string, bool) {
	in := input.(*SelectObjectContentInput)
	if in.Bucket == nil {
		return nil, false
	}
	return in.Bucket, true
}
func addSelectObjectContentUpdateEndpoint(stack *middleware.Stack, options Options) error {
	return s3cust.UpdateEndpoint(stack, s3cust.UpdateEndpointOptions{
		Accessor: s3cust.UpdateEndpointParameterAccessor{
			GetBucketFromInput: getSelectObjectContentBucketMember,
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

// SelectObjectContentEventStream provides the event stream handling for the SelectObjectContent operation.
//
// For testing and mocking the event stream this type should be initialized via
// the NewSelectObjectContentEventStream constructor function. Using the functional options
// to pass in nested mock behavior.
type SelectObjectContentEventStream struct {
	// SelectObjectContentEventStreamReader is the EventStream reader for the
	// SelectObjectContentEventStream events. This value is automatically set by the
	// SDK when the API call is made Use this member when unit testing your code with
	// the SDK to mock out the EventStream Reader.
	//
	// Must not be nil.
	Reader SelectObjectContentEventStreamReader

	done      chan struct{}
	closeOnce sync.Once
	err       *smithysync.OnceErr
}

// NewSelectObjectContentEventStream initializes an SelectObjectContentEventStream.
// This function should only be used for testing and mocking the SelectObjectContentEventStream
// stream within your application.
//
// The Reader member must be set before reading events from the stream.
func NewSelectObjectContentEventStream(optFns ...func(*SelectObjectContentEventStream)) *SelectObjectContentEventStream {
	es := &SelectObjectContentEventStream{
		done: make(chan struct{}),
		err:  smithysync.NewOnceErr(),
	}
	for _, fn := range optFns {
		fn(es)
	}
	return es
}

// Events returns a channel to read events from.
func (es *SelectObjectContentEventStream) Events() <-chan types.SelectObjectContentEventStream {
	return es.Reader.Events()
}

// Close closes the stream. This will also cause the stream to be closed.
// Close must be called when done using the stream API. Not calling Close
// may result in resource leaks.
//
// Will close the underlying EventStream writer and reader, and no more events can be
// sent or received.
func (es *SelectObjectContentEventStream) Close() error {
	es.closeOnce.Do(es.safeClose)
	return es.Err()
}

func (es *SelectObjectContentEventStream) safeClose() {
	close(es.done)

	es.Reader.Close()
}

// Err returns any error that occurred while reading or writing EventStream Events
// from the service API's response. Returns nil if there were no errors.
func (es *SelectObjectContentEventStream) Err() error {
	if err := es.err.Err(); err != nil {
		return err
	}

	if err := es.Reader.Err(); err != nil {
		return err
	}

	return nil
}

func (es *SelectObjectContentEventStream) waitStreamClose() {
	type errorSet interface {
		ErrorSet() <-chan struct{}
	}

	var outputErrCh <-chan struct{}
	if v, ok := es.Reader.(errorSet); ok {
		outputErrCh = v.ErrorSet()
	}
	var outputClosedCh <-chan struct{}
	if v, ok := es.Reader.(interface{ Closed() <-chan struct{} }); ok {
		outputClosedCh = v.Closed()
	}

	select {
	case <-es.done:
	case <-outputErrCh:
		es.err.SetError(es.Reader.Err())
		es.Close()

	case <-outputClosedCh:
		if err := es.Reader.Err(); err != nil {
			es.err.SetError(es.Reader.Err())
		}
		es.Close()

	}
}
