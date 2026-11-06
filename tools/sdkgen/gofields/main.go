// Command gofields prints the struct fields and method names of the types in
// one Go file as JSON, so tools/sdkgen/sdkgen.py can build the Go resource
// layer on top of the oapi-codegen models without re-deriving their names.
//
//	go run ./tools/sdkgen/gofields models.go > fields.json
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"go/ast"
	"go/parser"
	"go/printer"
	"go/token"
	"os"
	"reflect"
	"strings"
)

type field struct {
	Name string `json:"name"`
	Type string `json:"type"`
	JSON string `json:"json,omitempty"`
	Form string `json:"form,omitempty"`
}

type typeInfo struct {
	Kind    string   `json:"kind"` // struct | alias | other
	Fields  []field  `json:"fields,omitempty"`
	Target  string   `json:"target,omitempty"`
	Methods []string `json:"methods,omitempty"`
}

func main() {
	if err := run(os.Args[1]); err != nil {
		fmt.Fprintln(os.Stderr, "gofields:", err)
		os.Exit(1)
	}
}

func run(path string) error {
	fset := token.NewFileSet()
	file, err := parser.ParseFile(fset, path, nil, 0)
	if err != nil {
		return err
	}
	expr := func(e ast.Expr) string {
		var b bytes.Buffer
		_ = printer.Fprint(&b, fset, e)
		return b.String()
	}
	types := map[string]*typeInfo{}
	for _, decl := range file.Decls {
		switch d := decl.(type) {
		case *ast.GenDecl:
			for _, spec := range d.Specs {
				ts, ok := spec.(*ast.TypeSpec)
				if !ok {
					continue
				}
				info := &typeInfo{Kind: "other"}
				if ts.Assign.IsValid() {
					info.Kind, info.Target = "alias", expr(ts.Type)
				} else if st, ok := ts.Type.(*ast.StructType); ok {
					info.Kind = "struct"
					for _, f := range st.Fields.List {
						tag := ""
						if f.Tag != nil {
							tag = strings.Trim(f.Tag.Value, "`")
						}
						st := reflect.StructTag(tag)
						for _, n := range f.Names {
							info.Fields = append(info.Fields, field{
								Name: n.Name, Type: expr(f.Type),
								JSON: strings.Split(st.Get("json"), ",")[0],
								Form: strings.Split(st.Get("form"), ",")[0],
							})
						}
					}
				} else {
					info.Target = expr(ts.Type)
				}
				types[ts.Name.Name] = info
			}
		case *ast.FuncDecl:
			if d.Recv == nil || len(d.Recv.List) != 1 {
				continue
			}
			recv := strings.TrimPrefix(expr(d.Recv.List[0].Type), "*")
			if info := types[recv]; info != nil {
				info.Methods = append(info.Methods, d.Name.Name)
			} else {
				types[recv] = &typeInfo{Kind: "pending", Methods: []string{d.Name.Name}}
			}
		}
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", " ")
	return enc.Encode(types)
}
