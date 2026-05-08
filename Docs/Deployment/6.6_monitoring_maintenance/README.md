# Monitoring & Maintenance

This directory contains monitoring and maintenance scripts for the deployed application.

## Health Checks

### Running Health Checks

```bash
python Docs/Deployment/6.6_monitoring_maintenance/health_check.py
```

This script checks the health of:
- Backend API (http://localhost:8000/api/health)
- Frontend UI (http://localhost:8501/_stcore/health)

### Health Check Results

The script returns:
- ✅ Healthy: Service is responding correctly
- ❌ Unhealthy: Service is not responding or returning errors
- ❌ Error: Connection or timeout error

## Logging

### Logging Configuration

The application uses structured JSON logging for production environments.

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical error messages

### Log Storage

- **Local**: Console output and optional file logging
- **Docker**: Container logs accessible via `docker logs`
- **AWS**: CloudWatch Logs (configured in ECS task definition)

### Using the Logging Configuration

```python
from Docs.Deployment.6.6_monitoring_maintenance.logging_config import setup_logging, get_logger

# Setup logging
logger = setup_logging(level="INFO", format_type="json")

# Get logger
logger = get_logger(__name__)
logger.info("Application started")
```

## Monitoring Metrics

### Key Metrics to Monitor

1. **Response Time**
   - Target: <3 seconds for 90th percentile
   - Alert: >5 seconds for 95th percentile

2. **Error Rate**
   - Target: <1% of requests
   - Alert: >5% of requests

3. **Cache Hit Rate**
   - Target: >70%
   - Alert: <50%

4. **CPU/Memory Usage**
   - Target: <80% utilization
   - Alert: >90% utilization

5. **Database Performance**
   - Query latency
   - Connection pool usage

### CloudWatch Alarms

Recommended CloudWatch alarms:
- CPU utilization > 80%
- Memory utilization > 80%
- Error rate > 5%
- Response time > 5s

## Maintenance Tasks

### Daily
- Review error logs
- Check health status
- Monitor resource usage

### Weekly
- Review performance metrics
- Check for security updates
- Review cache efficiency

### Monthly
- Review and rotate logs
- Update dependencies
- Review costs
- Backup configurations

### Quarterly
- Security audit
- Performance review
- Capacity planning
- Disaster recovery testing

## Troubleshooting

### High CPU Usage
- Check for infinite loops
- Review query complexity
- Scale up resources

### High Memory Usage
- Check for memory leaks
- Review cache size
- Scale up resources

### Slow Response Times
- Check database queries
- Review network latency
- Check cache hit rate
- Scale horizontally

### High Error Rate
- Review error logs
- Check API key validity
- Verify database connectivity
- Review recent deployments
