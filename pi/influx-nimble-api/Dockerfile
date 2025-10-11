FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY main.go ./
RUN go mod tidy
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-w -s" -o api .

FROM scratch
COPY --from=builder /app/api /api
EXPOSE 8080
ENTRYPOINT ["/api"]
