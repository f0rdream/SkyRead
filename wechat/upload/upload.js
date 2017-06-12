const client = require('scp2')

const query = {
  host: '115.159.185.170',
  username: 'ubuntu',
  privateKey: require('fs').readFileSync('upload/zongyu_ubuntu'),
  path: '/web/SkyRead/backend/Backendapi/wechat/static'
}

client.scp('dist/static', query, function (err) {
  if (err) {
    console.log(err)
  } else {
    console.log('Sync1 succeed!')
  }
})

const query2 = {
  host: '115.159.185.170',
  username: 'ubuntu',
  privateKey: require('fs').readFileSync('upload/zongyu_ubuntu'),
  path: '/web/SkyRead/backend/Backendapi/wechat/templates/index.html'
}

client.scp('dist/index.html', query2, function (err) {
  if (err) {
    console.log(err)
  } else {
    console.log('Sync2 succeed!')
  }
})
