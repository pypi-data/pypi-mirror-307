// Code generated by smithy-go-codegen DO NOT EDIT.

package endpoints

import (
	"fmt"
	"github.com/aws/aws-sdk-go-v2/aws"
	endpoints "github.com/aws/aws-sdk-go-v2/internal/endpoints/v2"
	"github.com/aws/smithy-go/logging"
	"regexp"
	"strings"
)

// Options is the endpoint resolver configuration options
type Options struct {
	// Logger is a logging implementation that log events should be sent to.
	Logger logging.Logger

	// LogDeprecated indicates that deprecated endpoints should be logged to the
	// provided logger.
	LogDeprecated bool

	// ResolvedRegion is used to override the region to be resolved, rather then the
	// using the value passed to the ResolveEndpoint method. This value is used by the
	// SDK to translate regions like fips-us-east-1 or us-east-1-fips to an alternative
	// name. You must not set this value directly in your application.
	ResolvedRegion string

	// DisableHTTPS informs the resolver to return an endpoint that does not use the
	// HTTPS scheme.
	DisableHTTPS bool

	// UseDualStackEndpoint specifies the resolver must resolve a dual-stack endpoint.
	UseDualStackEndpoint aws.DualStackEndpointState

	// UseFIPSEndpoint specifies the resolver must resolve a FIPS endpoint.
	UseFIPSEndpoint aws.FIPSEndpointState
}

func (o Options) GetResolvedRegion() string {
	return o.ResolvedRegion
}

func (o Options) GetDisableHTTPS() bool {
	return o.DisableHTTPS
}

func (o Options) GetUseDualStackEndpoint() aws.DualStackEndpointState {
	return o.UseDualStackEndpoint
}

func (o Options) GetUseFIPSEndpoint() aws.FIPSEndpointState {
	return o.UseFIPSEndpoint
}

func transformToSharedOptions(options Options) endpoints.Options {
	return endpoints.Options{
		Logger:               options.Logger,
		LogDeprecated:        options.LogDeprecated,
		ResolvedRegion:       options.ResolvedRegion,
		DisableHTTPS:         options.DisableHTTPS,
		UseDualStackEndpoint: options.UseDualStackEndpoint,
		UseFIPSEndpoint:      options.UseFIPSEndpoint,
	}
}

// Resolver S3 endpoint resolver
type Resolver struct {
	partitions endpoints.Partitions
}

// ResolveEndpoint resolves the service endpoint for the given region and options
func (r *Resolver) ResolveEndpoint(region string, options Options) (endpoint aws.Endpoint, err error) {
	if len(region) == 0 {
		return endpoint, &aws.MissingRegionError{}
	}

	opt := transformToSharedOptions(options)
	return r.partitions.ResolveEndpoint(region, opt)
}

// New returns a new Resolver
func New() *Resolver {
	return &Resolver{
		partitions: defaultPartitions,
	}
}

var partitionRegexp = struct {
	Aws      *regexp.Regexp
	AwsCn    *regexp.Regexp
	AwsIso   *regexp.Regexp
	AwsIsoB  *regexp.Regexp
	AwsIsoE  *regexp.Regexp
	AwsIsoF  *regexp.Regexp
	AwsUsGov *regexp.Regexp
}{

	Aws:      regexp.MustCompile("^(us|eu|ap|sa|ca|me|af|il|mx)\\-\\w+\\-\\d+$"),
	AwsCn:    regexp.MustCompile("^cn\\-\\w+\\-\\d+$"),
	AwsIso:   regexp.MustCompile("^us\\-iso\\-\\w+\\-\\d+$"),
	AwsIsoB:  regexp.MustCompile("^us\\-isob\\-\\w+\\-\\d+$"),
	AwsIsoE:  regexp.MustCompile("^eu\\-isoe\\-\\w+\\-\\d+$"),
	AwsIsoF:  regexp.MustCompile("^us\\-isof\\-\\w+\\-\\d+$"),
	AwsUsGov: regexp.MustCompile("^us\\-gov\\-\\w+\\-\\d+$"),
}

var defaultPartitions = endpoints.Partitions{
	{
		ID: "aws",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.{region}.amazonaws.com",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.amazonaws.com",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.{region}.amazonaws.com",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.amazonaws.com",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
		},
		RegionRegex:    partitionRegexp.Aws,
		IsRegionalized: true,
		Endpoints: endpoints.Endpoints{
			endpoints.EndpointKey{
				Region: "af-south-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "af-south-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.af-south-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-east-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-east-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-east-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-northeast-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.ap-northeast-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "ap-northeast-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.ap-northeast-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "ap-northeast-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-northeast-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-northeast-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-northeast-3",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-northeast-3",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-northeast-3.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-south-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-south-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-south-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-south-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-south-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-south-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-southeast-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.ap-southeast-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "ap-southeast-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.ap-southeast-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "ap-southeast-2",
			}: endpoints.Endpoint{
				Hostname:          "s3.ap-southeast-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "ap-southeast-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.ap-southeast-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "ap-southeast-3",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-southeast-3",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-southeast-3.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-southeast-4",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-southeast-4",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-southeast-4.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ap-southeast-5",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ap-southeast-5",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ap-southeast-5.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "aws-global",
			}: endpoints.Endpoint{
				Hostname:          "s3.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
				CredentialScope: endpoints.CredentialScope{
					Region: "us-east-1",
				},
			},
			endpoints.EndpointKey{
				Region: "ca-central-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ca-central-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname: "s3-fips.ca-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "ca-central-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname: "s3-fips.dualstack.ca-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "ca-central-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ca-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "ca-west-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "ca-west-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname: "s3-fips.ca-west-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "ca-west-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname: "s3-fips.dualstack.ca-west-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "ca-west-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.ca-west-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-central-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-central-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-central-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-central-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-central-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-north-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-north-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-north-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-south-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-south-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-south-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-south-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-south-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-south-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-west-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.eu-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "eu-west-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.eu-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "eu-west-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-west-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-west-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "eu-west-3",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "eu-west-3",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.eu-west-3.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "fips-ca-central-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.ca-central-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "ca-central-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-ca-west-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.ca-west-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "ca-west-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-east-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-east-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-east-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-east-2",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-east-2.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-east-2",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-west-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-west-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-west-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-west-2",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-west-2.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-west-2",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "il-central-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "il-central-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.il-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "me-central-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "me-central-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.me-central-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "me-south-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "me-south-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.me-south-1.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "s3-external-1",
			}: endpoints.Endpoint{
				Hostname:          "s3-external-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
				CredentialScope: endpoints.CredentialScope{
					Region: "us-east-1",
				},
			},
			endpoints.EndpointKey{
				Region: "sa-east-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.sa-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "sa-east-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.sa-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "us-east-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.us-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-east-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.us-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-east-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.us-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-east-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.us-east-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "us-east-2",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "us-east-2",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname: "s3-fips.dualstack.us-east-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "us-east-2",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname: "s3-fips.us-east-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region:  "us-east-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.us-east-2.amazonaws.com",
			},
			endpoints.EndpointKey{
				Region: "us-west-1",
			}: endpoints.Endpoint{
				Hostname:          "s3.us-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.us-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.us-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.us-west-1.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region: "us-west-2",
			}: endpoints.Endpoint{
				Hostname:          "s3.us-west-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-2",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.us-west-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-2",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.us-west-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-west-2",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.us-west-2.amazonaws.com",
				SignatureVersions: []string{"s3", "s3v4"},
			},
		},
	},
	{
		ID: "aws-cn",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.{region}.amazonaws.com.cn",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.amazonaws.com.cn",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.{region}.api.amazonwebservices.com.cn",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.amazonaws.com.cn",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsCn,
		IsRegionalized: true,
		Endpoints: endpoints.Endpoints{
			endpoints.EndpointKey{
				Region: "cn-north-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "cn-north-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.cn-north-1.amazonaws.com.cn",
			},
			endpoints.EndpointKey{
				Region: "cn-northwest-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "cn-northwest-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname: "s3.dualstack.cn-northwest-1.amazonaws.com.cn",
			},
		},
	},
	{
		ID: "aws-iso",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.c2s.ic.gov",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.c2s.ic.gov",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsIso,
		IsRegionalized: true,
		Endpoints: endpoints.Endpoints{
			endpoints.EndpointKey{
				Region: "fips-us-iso-east-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-iso-east-1.c2s.ic.gov",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-iso-east-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-iso-west-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-iso-west-1.c2s.ic.gov",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-iso-west-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "us-iso-east-1",
			}: endpoints.Endpoint{
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-iso-east-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.us-iso-east-1.c2s.ic.gov",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			endpoints.EndpointKey{
				Region:  "us-iso-east-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.us-iso-east-1.c2s.ic.gov",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			endpoints.EndpointKey{
				Region: "us-iso-west-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "us-iso-west-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname: "s3-fips.dualstack.us-iso-west-1.c2s.ic.gov",
			},
			endpoints.EndpointKey{
				Region:  "us-iso-west-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname: "s3-fips.us-iso-west-1.c2s.ic.gov",
			},
		},
	},
	{
		ID: "aws-iso-b",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.sc2s.sgov.gov",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.sc2s.sgov.gov",
				Protocols:         []string{"http", "https"},
				SignatureVersions: []string{"s3v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsIsoB,
		IsRegionalized: true,
		Endpoints: endpoints.Endpoints{
			endpoints.EndpointKey{
				Region: "fips-us-isob-east-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-isob-east-1.sc2s.sgov.gov",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-isob-east-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "us-isob-east-1",
			}: endpoints.Endpoint{},
			endpoints.EndpointKey{
				Region:  "us-isob-east-1",
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname: "s3-fips.dualstack.us-isob-east-1.sc2s.sgov.gov",
			},
			endpoints.EndpointKey{
				Region:  "us-isob-east-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname: "s3-fips.us-isob-east-1.sc2s.sgov.gov",
			},
		},
	},
	{
		ID: "aws-iso-e",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.cloud.adc-e.uk",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.cloud.adc-e.uk",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsIsoE,
		IsRegionalized: true,
	},
	{
		ID: "aws-iso-f",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.csp.hci.ic.gov",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.csp.hci.ic.gov",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsIsoF,
		IsRegionalized: true,
	},
	{
		ID: "aws-us-gov",
		Defaults: map[endpoints.DefaultKey]endpoints.Endpoint{
			{
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:          "s3.dualstack.{region}.amazonaws.com",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3", "s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:          "s3-fips.{region}.amazonaws.com",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3", "s3v4"},
			},
			{
				Variant: endpoints.FIPSVariant | endpoints.DualStackVariant,
			}: {
				Hostname:          "s3-fips.dualstack.{region}.amazonaws.com",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3", "s3v4"},
			},
			{
				Variant: 0,
			}: {
				Hostname:          "s3.{region}.amazonaws.com",
				Protocols:         []string{"https"},
				SignatureVersions: []string{"s3", "s3v4"},
			},
		},
		RegionRegex:    partitionRegexp.AwsUsGov,
		IsRegionalized: true,
		Endpoints: endpoints.Endpoints{
			endpoints.EndpointKey{
				Region: "fips-us-gov-east-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-gov-east-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-gov-east-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "fips-us-gov-west-1",
			}: endpoints.Endpoint{
				Hostname: "s3-fips.us-gov-west-1.amazonaws.com",
				CredentialScope: endpoints.CredentialScope{
					Region: "us-gov-west-1",
				},
				Deprecated: aws.TrueTernary,
			},
			endpoints.EndpointKey{
				Region: "us-gov-east-1",
			}: endpoints.Endpoint{
				Hostname:  "s3.us-gov-east-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
			endpoints.EndpointKey{
				Region:  "us-gov-east-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:  "s3-fips.us-gov-east-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
			endpoints.EndpointKey{
				Region:  "us-gov-east-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:  "s3.dualstack.us-gov-east-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
			endpoints.EndpointKey{
				Region: "us-gov-west-1",
			}: endpoints.Endpoint{
				Hostname:  "s3.us-gov-west-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
			endpoints.EndpointKey{
				Region:  "us-gov-west-1",
				Variant: endpoints.FIPSVariant,
			}: {
				Hostname:  "s3-fips.us-gov-west-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
			endpoints.EndpointKey{
				Region:  "us-gov-west-1",
				Variant: endpoints.DualStackVariant,
			}: {
				Hostname:  "s3.dualstack.us-gov-west-1.amazonaws.com",
				Protocols: []string{"http", "https"},
			},
		},
	},
}

// GetDNSSuffix returns the dnsSuffix URL component for the given partition id
func GetDNSSuffix(id string, options Options) (string, error) {
	variant := transformToSharedOptions(options).GetEndpointVariant()
	switch {
	case strings.EqualFold(id, "aws"):
		switch variant {
		case endpoints.DualStackVariant:
			return "amazonaws.com", nil

		case endpoints.FIPSVariant:
			return "amazonaws.com", nil

		case endpoints.FIPSVariant | endpoints.DualStackVariant:
			return "amazonaws.com", nil

		case 0:
			return "amazonaws.com", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-cn"):
		switch variant {
		case endpoints.DualStackVariant:
			return "amazonaws.com.cn", nil

		case endpoints.FIPSVariant:
			return "amazonaws.com.cn", nil

		case endpoints.FIPSVariant | endpoints.DualStackVariant:
			return "api.amazonwebservices.com.cn", nil

		case 0:
			return "amazonaws.com.cn", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-iso"):
		switch variant {
		case endpoints.FIPSVariant:
			return "c2s.ic.gov", nil

		case 0:
			return "c2s.ic.gov", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-iso-b"):
		switch variant {
		case endpoints.FIPSVariant:
			return "sc2s.sgov.gov", nil

		case 0:
			return "sc2s.sgov.gov", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-iso-e"):
		switch variant {
		case endpoints.FIPSVariant:
			return "cloud.adc-e.uk", nil

		case 0:
			return "cloud.adc-e.uk", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-iso-f"):
		switch variant {
		case endpoints.FIPSVariant:
			return "csp.hci.ic.gov", nil

		case 0:
			return "csp.hci.ic.gov", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	case strings.EqualFold(id, "aws-us-gov"):
		switch variant {
		case endpoints.DualStackVariant:
			return "amazonaws.com", nil

		case endpoints.FIPSVariant:
			return "amazonaws.com", nil

		case endpoints.FIPSVariant | endpoints.DualStackVariant:
			return "amazonaws.com", nil

		case 0:
			return "amazonaws.com", nil

		default:
			return "", fmt.Errorf("unsupported endpoint variant %v, in partition %s", variant, id)

		}

	default:
		return "", fmt.Errorf("unknown partition")

	}
}

// GetDNSSuffixFromRegion returns the DNS suffix for the provided region and
// options.
func GetDNSSuffixFromRegion(region string, options Options) (string, error) {
	switch {
	case partitionRegexp.Aws.MatchString(region):
		return GetDNSSuffix("aws", options)

	case partitionRegexp.AwsCn.MatchString(region):
		return GetDNSSuffix("aws-cn", options)

	case partitionRegexp.AwsIso.MatchString(region):
		return GetDNSSuffix("aws-iso", options)

	case partitionRegexp.AwsIsoB.MatchString(region):
		return GetDNSSuffix("aws-iso-b", options)

	case partitionRegexp.AwsIsoE.MatchString(region):
		return GetDNSSuffix("aws-iso-e", options)

	case partitionRegexp.AwsIsoF.MatchString(region):
		return GetDNSSuffix("aws-iso-f", options)

	case partitionRegexp.AwsUsGov.MatchString(region):
		return GetDNSSuffix("aws-us-gov", options)

	default:
		return GetDNSSuffix("aws", options)

	}
}
