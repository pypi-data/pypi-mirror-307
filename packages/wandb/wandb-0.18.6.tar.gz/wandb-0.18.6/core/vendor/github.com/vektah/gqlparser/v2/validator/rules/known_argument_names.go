package rules

import (
	"github.com/vektah/gqlparser/v2/ast"

	//nolint:revive // Validator rules each use dot imports for convenience.
	. "github.com/vektah/gqlparser/v2/validator"
)

var KnownArgumentNamesRule = Rule{
	Name: "KnownArgumentNames",
	RuleFunc: func(observers *Events, addError AddErrFunc) {
		// A GraphQL field is only valid if all supplied arguments are defined by that field.
		observers.OnField(func(walker *Walker, field *ast.Field) {
			if field.Definition == nil || field.ObjectDefinition == nil {
				return
			}
			for _, arg := range field.Arguments {
				def := field.Definition.Arguments.ForName(arg.Name)
				if def != nil {
					continue
				}

				var suggestions []string
				for _, argDef := range field.Definition.Arguments {
					suggestions = append(suggestions, argDef.Name)
				}

				addError(
					Message(`Unknown argument "%s" on field "%s.%s".`, arg.Name, field.ObjectDefinition.Name, field.Name),
					SuggestListQuoted("Did you mean", arg.Name, suggestions),
					At(field.Position),
				)
			}
		})

		observers.OnDirective(func(walker *Walker, directive *ast.Directive) {
			if directive.Definition == nil {
				return
			}
			for _, arg := range directive.Arguments {
				def := directive.Definition.Arguments.ForName(arg.Name)
				if def != nil {
					continue
				}

				var suggestions []string
				for _, argDef := range directive.Definition.Arguments {
					suggestions = append(suggestions, argDef.Name)
				}

				addError(
					Message(`Unknown argument "%s" on directive "@%s".`, arg.Name, directive.Name),
					SuggestListQuoted("Did you mean", arg.Name, suggestions),
					At(directive.Position),
				)
			}
		})
	},
}

func init() {
	AddRule(KnownArgumentNamesRule.Name, KnownArgumentNamesRule.RuleFunc)
}
