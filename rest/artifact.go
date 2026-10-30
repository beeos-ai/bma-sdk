package rest

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"strings"
)

// ArtifactContent is an open artifact content response. Close it after use.
type ArtifactContent struct {
	ContentType   string
	ContentLength int64
	Body          io.ReadCloser
}

// OpenArtifactContent opens GET .../artifacts/{artifactID}/content without
// buffering the body. Callers that need integrity checks should use
// DownloadArtifact instead.
func (c *Client) OpenArtifactContent(ctx context.Context, orgID, projectID, agentID, artifactID string) (*ArtifactContent, error) {
	req, err := NewGetArtifactContentRequest(c.server, orgID, projectID, agentID, artifactID)
	if err != nil {
		return nil, fmt.Errorf("rest: build artifact request: %w", err)
	}
	if err := c.authenticate(ctx, req); err != nil {
		return nil, err
	}
	req.Header.Set("Accept", "application/octet-stream")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("rest: open artifact content: %w", err)
	}
	if resp.StatusCode != http.StatusOK {
		return nil, newAPIErrorFromResponse(resp)
	}
	return &ArtifactContent{
		ContentType:   resp.Header.Get("Content-Type"),
		ContentLength: resp.ContentLength,
		Body:          resp.Body,
	}, nil
}

// DownloadArtifact streams artifact content into w and verifies the size and
// sha256 digest recorded on artifact. maxBytes is an explicit product limit.
// The caller must discard partial output when this method returns an error.
func (c *Client) DownloadArtifact(ctx context.Context, artifact Artifact, maxBytes int64, w io.Writer) error {
	if maxBytes <= 0 || w == nil {
		return fmt.Errorf("rest: maxBytes and writer are required")
	}
	if artifact.AgentId == "" || artifact.Id == "" {
		return fmt.Errorf("rest: artifact agent_id and id are required")
	}
	if artifact.SizeBytes == nil || *artifact.SizeBytes < 0 || *artifact.SizeBytes > maxBytes {
		return fmt.Errorf("rest: artifact size is missing or exceeds maxBytes")
	}
	if artifact.Digest == nil || !strings.HasPrefix(*artifact.Digest, "sha256:") {
		return fmt.Errorf("rest: artifact digest must be sha256:<hex>")
	}
	expected, err := hex.DecodeString(strings.TrimPrefix(*artifact.Digest, "sha256:"))
	if err != nil || len(expected) != sha256.Size {
		return fmt.Errorf("rest: artifact digest is not a sha256 hex digest")
	}

	content, err := c.OpenArtifactContent(ctx, artifact.OrgId, artifact.ProjectId, artifact.AgentId, artifact.Id)
	if err != nil {
		return err
	}
	defer content.Body.Close()

	hasher := sha256.New()
	n, err := io.Copy(io.MultiWriter(w, hasher), io.LimitReader(content.Body, *artifact.SizeBytes+1))
	if err != nil {
		return fmt.Errorf("rest: read artifact content: %w", err)
	}
	if n != *artifact.SizeBytes {
		return fmt.Errorf("rest: artifact size = %d, want %d", n, *artifact.SizeBytes)
	}
	if !equalBytes(hasher.Sum(nil), expected) {
		return fmt.Errorf("rest: artifact digest mismatch")
	}
	return nil
}

func equalBytes(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	var diff byte
	for i := range a {
		diff |= a[i] ^ b[i]
	}
	return diff == 0
}
