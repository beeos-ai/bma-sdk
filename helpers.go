package bma

import "io"

// NewFile names a reader for a multipart file field; the name is sent as
// the part's filename (an *os.File is named already).
func NewFile(r io.Reader, filename string) io.Reader { return &namedReader{r, filename, ""} }

// NewFileWithContentType is NewFile with an explicit part content type.
func NewFileWithContentType(r io.Reader, filename, contentType string) io.Reader {
	return &namedReader{r, filename, contentType}
}

type namedReader struct {
	io.Reader
	name        string
	contentType string
}

func (n *namedReader) Name() string        { return n.name }
func (n *namedReader) ContentType() string { return n.contentType }

// NewTextContentBlock builds a text content block.
func NewTextContentBlock(text string) TextContentBlock {
	return TextContentBlock{Type: TextContentBlockType("text"), Text: text}
}

// NewInlineMediaContentBlock builds an inline media block; data is the raw
// file content (base64 on the wire).
func NewInlineMediaContentBlock(mediaType, filename string, data []byte) InlineMediaContentBlock {
	block := InlineMediaContentBlock{Type: InlineMediaContentBlockType("media"), MediaType: InlineMediaContentBlockMediaType(mediaType), Data: data}
	if filename != "" {
		block.Filename = &filename
	}
	return block
}

// NewTextInputBlock builds a text block of AgentInputNewParams.ContentBlocks.
func NewTextInputBlock(text string) CreateAgentInputContentBlock {
	var block CreateAgentInputContentBlock
	_ = block.FromTextContentBlock(NewTextContentBlock(text))
	return block
}

// NewMediaInputBlock builds an inline media block of AgentInputNewParams.ContentBlocks.
func NewMediaInputBlock(mediaType, filename string, data []byte) CreateAgentInputContentBlock {
	var block CreateAgentInputContentBlock
	_ = block.FromInlineMediaContentBlock(NewInlineMediaContentBlock(mediaType, filename, data))
	return block
}
